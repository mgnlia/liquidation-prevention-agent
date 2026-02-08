const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

// Sepolia testnet addresses
const SEPOLIA_ADDRESSES = {
  AAVE_POOL: "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951",
  AAVE_POOL_ADDRESSES_PROVIDER: "0x0496275d34753A48320CA58103d5220d394FF77F",
  COMPOUND_COMET_USDC: "0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e",
};

async function main() {
  console.log("🚀 Starting deployment to Sepolia testnet...\n");

  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString(), "\n");

  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {},
  };

  // Deploy AaveV3Adapter
  console.log("📝 Deploying AaveV3Adapter...");
  const AaveV3Adapter = await hre.ethers.getContractFactory("AaveV3Adapter");
  const aaveAdapter = await AaveV3Adapter.deploy(SEPOLIA_ADDRESSES.AAVE_POOL);
  await aaveAdapter.deployed();
  console.log("✅ AaveV3Adapter deployed to:", aaveAdapter.address);
  deploymentInfo.contracts.aaveAdapter = aaveAdapter.address;

  // Deploy CompoundV3Adapter
  console.log("\n📝 Deploying CompoundV3Adapter...");
  const CompoundV3Adapter = await hre.ethers.getContractFactory("CompoundV3Adapter");
  const compoundAdapter = await CompoundV3Adapter.deploy(SEPOLIA_ADDRESSES.COMPOUND_COMET_USDC);
  await compoundAdapter.deployed();
  console.log("✅ CompoundV3Adapter deployed to:", compoundAdapter.address);
  deploymentInfo.contracts.compoundAdapter = compoundAdapter.address;

  // Deploy FlashLoanRebalancer
  console.log("\n📝 Deploying FlashLoanRebalancer...");
  const FlashLoanRebalancer = await hre.ethers.getContractFactory("FlashLoanRebalancer");
  const rebalancer = await FlashLoanRebalancer.deploy(
    SEPOLIA_ADDRESSES.AAVE_POOL_ADDRESSES_PROVIDER,
    SEPOLIA_ADDRESSES.AAVE_POOL,
    deployer.address // Initial executor
  );
  await rebalancer.deployed();
  console.log("✅ FlashLoanRebalancer deployed to:", rebalancer.address);
  deploymentInfo.contracts.rebalancer = rebalancer.address;

  // Deploy LiquidationPrevention
  console.log("\n📝 Deploying LiquidationPrevention...");
  const LiquidationPrevention = await hre.ethers.getContractFactory("LiquidationPrevention");
  const liquidationPrevention = await LiquidationPrevention.deploy(
    aaveAdapter.address,
    compoundAdapter.address,
    rebalancer.address
  );
  await liquidationPrevention.deployed();
  console.log("✅ LiquidationPrevention deployed to:", liquidationPrevention.address);
  deploymentInfo.contracts.liquidationPrevention = liquidationPrevention.address;

  // Grant roles
  console.log("\n🔐 Setting up roles...");
  const AGENT_ROLE = await liquidationPrevention.AGENT_ROLE();
  const MONITOR_ROLE = await liquidationPrevention.MONITOR_ROLE();
  
  await liquidationPrevention.grantRole(AGENT_ROLE, deployer.address);
  await liquidationPrevention.grantRole(MONITOR_ROLE, deployer.address);
  console.log("✅ Roles granted to deployer");

  // Update rebalancer executor to LiquidationPrevention contract
  console.log("\n🔗 Linking rebalancer to LiquidationPrevention...");
  await rebalancer.setExecutor(liquidationPrevention.address);
  console.log("✅ Rebalancer executor updated");

  // Save deployment info
  const deploymentsDir = path.join(__dirname, "../deployments");
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir);
  }

  const deploymentPath = path.join(
    deploymentsDir,
    `${hre.network.name}-${Date.now()}.json`
  );
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log("\n💾 Deployment info saved to:", deploymentPath);

  // Summary
  console.log("\n" + "=".repeat(60));
  console.log("🎉 DEPLOYMENT COMPLETE!");
  console.log("=".repeat(60));
  console.log("\nContract Addresses:");
  console.log("  AaveV3Adapter:          ", aaveAdapter.address);
  console.log("  CompoundV3Adapter:      ", compoundAdapter.address);
  console.log("  FlashLoanRebalancer:    ", rebalancer.address);
  console.log("  LiquidationPrevention:  ", liquidationPrevention.address);
  console.log("\nNext steps:");
  console.log("  1. Verify contracts on Etherscan:");
  console.log("     npx hardhat verify --network sepolia <address> <constructor-args>");
  console.log("  2. Update agent/.env with contract addresses");
  console.log("  3. Update subgraph/subgraph.yaml with contract addresses");
  console.log("=".repeat(60) + "\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
