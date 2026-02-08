const hre = require("hardhat");
require("dotenv").config();

async function main() {
  console.log("🚀 Deploying Liquidation Prevention System to Sepolia...\n");

  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  console.log("Account balance:", (await hre.ethers.provider.getBalance(deployer.address)).toString(), "\n");

  // Aave V3 Sepolia addresses
  const AAVE_POOL_ADDRESS_PROVIDER = process.env.AAVE_POOL_ADDRESS_PROVIDER || "0x012bAC54348C0E635dCAc9D5FB99f06F24136C9A";
  const AAVE_POOL = process.env.AAVE_POOL || "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951";
  
  // Compound V3 Sepolia (placeholder - update with actual address)
  const COMPOUND_COMET = process.env.COMPOUND_COMET_USDC || "0x0000000000000000000000000000000000000000";
  
  // AI Agent address (deployer for now, update later)
  const AI_AGENT = deployer.address;

  // Deploy AaveV3Adapter
  console.log("📦 Deploying AaveV3Adapter...");
  const AaveV3Adapter = await hre.ethers.getContractFactory("AaveV3Adapter");
  const aaveAdapter = await AaveV3Adapter.deploy(AAVE_POOL);
  await aaveAdapter.waitForDeployment();
  const aaveAdapterAddress = await aaveAdapter.getAddress();
  console.log("✅ AaveV3Adapter deployed to:", aaveAdapterAddress, "\n");

  // Deploy CompoundV3Adapter
  console.log("📦 Deploying CompoundV3Adapter...");
  const CompoundV3Adapter = await hre.ethers.getContractFactory("CompoundV3Adapter");
  const compoundAdapter = await CompoundV3Adapter.deploy(COMPOUND_COMET);
  await compoundAdapter.waitForDeployment();
  const compoundAdapterAddress = await compoundAdapter.getAddress();
  console.log("✅ CompoundV3Adapter deployed to:", compoundAdapterAddress, "\n");

  // Deploy FlashLoanRebalancer
  console.log("📦 Deploying FlashLoanRebalancer...");
  const FlashLoanRebalancer = await hre.ethers.getContractFactory("FlashLoanRebalancer");
  const rebalancer = await FlashLoanRebalancer.deploy(
    AAVE_POOL_ADDRESS_PROVIDER,
    AAVE_POOL,
    AI_AGENT
  );
  await rebalancer.waitForDeployment();
  const rebalancerAddress = await rebalancer.getAddress();
  console.log("✅ FlashLoanRebalancer deployed to:", rebalancerAddress, "\n");

  // Deploy LiquidationPrevention
  console.log("📦 Deploying LiquidationPrevention...");
  const LiquidationPrevention = await hre.ethers.getContractFactory("LiquidationPrevention");
  const liquidationPrevention = await LiquidationPrevention.deploy(
    aaveAdapterAddress,
    compoundAdapterAddress,
    rebalancerAddress,
    AI_AGENT
  );
  await liquidationPrevention.waitForDeployment();
  const liquidationPreventionAddress = await liquidationPrevention.getAddress();
  console.log("✅ LiquidationPrevention deployed to:", liquidationPreventionAddress, "\n");

  // Summary
  console.log("=" .repeat(60));
  console.log("🎉 DEPLOYMENT COMPLETE!");
  console.log("=" .repeat(60));
  console.log("\n📋 Contract Addresses:");
  console.log("  AaveV3Adapter:         ", aaveAdapterAddress);
  console.log("  CompoundV3Adapter:     ", compoundAdapterAddress);
  console.log("  FlashLoanRebalancer:   ", rebalancerAddress);
  console.log("  LiquidationPrevention: ", liquidationPreventionAddress);
  console.log("\n🔗 Network:", hre.network.name);
  console.log("👤 AI Agent:", AI_AGENT);
  console.log("\n💡 Next steps:");
  console.log("  1. Verify contracts on Etherscan: npx hardhat run scripts/verify.js --network sepolia");
  console.log("  2. Update agent/.env with contract addresses");
  console.log("  3. Test monitoring: node agent/monitor.js");
  console.log("=" .repeat(60));

  // Save deployment info
  const fs = require("fs");
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      AaveV3Adapter: aaveAdapterAddress,
      CompoundV3Adapter: compoundAdapterAddress,
      FlashLoanRebalancer: rebalancerAddress,
      LiquidationPrevention: liquidationPreventionAddress,
    },
    config: {
      aavePool: AAVE_POOL,
      aavePoolAddressProvider: AAVE_POOL_ADDRESS_PROVIDER,
      compoundComet: COMPOUND_COMET,
      aiAgent: AI_AGENT,
    },
  };

  fs.writeFileSync(
    "deployment-info.json",
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("\n💾 Deployment info saved to deployment-info.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
