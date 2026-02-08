const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

// Sepolia Aave V3 addresses
const SEPOLIA_AAVE_V3_POOL = "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951";
const SEPOLIA_AAVE_V3_POOL_ADDRESSES_PROVIDER = "0x012bAC54348C0E635dCAc9D5FB99f06F24136C9A";
const SEPOLIA_COMPOUND_V3_COMET_USDC = "0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e";

async function main() {
  console.log("\n🚀 Deploying Liquidation Prevention System to", hre.network.name, "...\n");

  const [deployer] = await hre.ethers.getSigners();
  const balance = await hre.ethers.provider.getBalance(deployer.address);

  console.log("📋 Deployment Configuration:");
  console.log("   Network:", hre.network.name, `(${hre.network.config.chainId})`);
  console.log("   Deployer:", deployer.address);
  console.log("   Balance:", hre.ethers.formatEther(balance), "ETH\n");

  if (balance < hre.ethers.parseEther("0.1")) {
    console.warn("⚠️  Warning: Low balance. Deployment may fail.\n");
  }

  // Get AI agent address from env or use deployer
  const aiAgentAddress = process.env.AI_AGENT_ADDRESS || deployer.address;
  console.log("🤖 AI Agent Address:", aiAgentAddress, "\n");

  console.log("📦 Deploying Contracts...\n");

  // 1. Deploy AaveV3Adapter
  console.log("1️⃣  Deploying AaveV3Adapter...");
  const AaveV3Adapter = await hre.ethers.getContractFactory("AaveV3Adapter");
  const aaveAdapter = await AaveV3Adapter.deploy(
    SEPOLIA_AAVE_V3_POOL_ADDRESSES_PROVIDER
  );
  await aaveAdapter.waitForDeployment();
  const aaveAdapterAddress = await aaveAdapter.getAddress();
  console.log("   ✅ AaveV3Adapter deployed to:", aaveAdapterAddress);

  // 2. Deploy CompoundV3Adapter
  console.log("\n2️⃣  Deploying CompoundV3Adapter...");
  const CompoundV3Adapter = await hre.ethers.getContractFactory("CompoundV3Adapter");
  const compoundAdapter = await CompoundV3Adapter.deploy(
    SEPOLIA_COMPOUND_V3_COMET_USDC
  );
  await compoundAdapter.waitForDeployment();
  const compoundAdapterAddress = await compoundAdapter.getAddress();
  console.log("   ✅ CompoundV3Adapter deployed to:", compoundAdapterAddress);

  // 3. Deploy FlashLoanRebalancer
  console.log("\n3️⃣  Deploying FlashLoanRebalancer...");
  const FlashLoanRebalancer = await hre.ethers.getContractFactory("FlashLoanRebalancer");
  const rebalancer = await FlashLoanRebalancer.deploy(
    SEPOLIA_AAVE_V3_POOL_ADDRESSES_PROVIDER
  );
  await rebalancer.waitForDeployment();
  const rebalancerAddress = await rebalancer.getAddress();
  console.log("   ✅ FlashLoanRebalancer deployed to:", rebalancerAddress);

  // 4. Deploy LiquidationPrevention
  console.log("\n4️⃣  Deploying LiquidationPrevention...");
  const LiquidationPrevention = await hre.ethers.getContractFactory("LiquidationPrevention");
  const liquidationPrevention = await LiquidationPrevention.deploy(
    aaveAdapterAddress,
    compoundAdapterAddress,
    rebalancerAddress,
    aiAgentAddress
  );
  await liquidationPrevention.waitForDeployment();
  const liquidationPreventionAddress = await liquidationPrevention.getAddress();
  console.log("   ✅ LiquidationPrevention deployed to:", liquidationPreventionAddress);

  // Save deployment addresses
  const deployment = {
    network: hre.network.name,
    chainId: hre.network.config.chainId,
    deployer: deployer.address,
    aiAgent: aiAgentAddress,
    timestamp: new Date().toISOString(),
    contracts: {
      LiquidationPrevention: liquidationPreventionAddress,
      AaveV3Adapter: aaveAdapterAddress,
      CompoundV3Adapter: compoundAdapterAddress,
      FlashLoanRebalancer: rebalancerAddress
    },
    protocolAddresses: {
      AaveV3Pool: SEPOLIA_AAVE_V3_POOL,
      AaveV3PoolAddressesProvider: SEPOLIA_AAVE_V3_POOL_ADDRESSES_PROVIDER,
      CompoundV3CometUSDC: SEPOLIA_COMPOUND_V3_COMET_USDC
    }
  };

  const deploymentsDir = path.join(__dirname, "../deployments");
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir, { recursive: true });
  }

  const filename = `${hre.network.name}-${Date.now()}.json`;
  const filepath = path.join(deploymentsDir, filename);
  fs.writeFileSync(filepath, JSON.stringify(deployment, null, 2));

  // Also save as latest
  const latestPath = path.join(deploymentsDir, `${hre.network.name}-latest.json`);
  fs.writeFileSync(latestPath, JSON.stringify(deployment, null, 2));

  console.log("\n💾 Deployment addresses saved to:");
  console.log("   ", filepath);
  console.log("   ", latestPath);

  console.log("\n✅ Deployment complete!\n");

  console.log("📝 Contract Addresses:");
  console.log(JSON.stringify(deployment.contracts, null, 2));

  console.log("\n📋 Next Steps:");
  console.log("1. Update agent/.env with these contract addresses");
  console.log("2. Run: npx hardhat run scripts/verify.js --network", hre.network.name);
  console.log("3. Start the AI agent: cd agent && python agent.py");

  console.log("\n🔗 Etherscan URLs:");
  const baseUrl = hre.network.name === "sepolia" 
    ? "https://sepolia.etherscan.io" 
    : "https://etherscan.io";
  console.log(`   LiquidationPrevention: ${baseUrl}/address/${liquidationPreventionAddress}`);
  console.log(`   AaveV3Adapter: ${baseUrl}/address/${aaveAdapterAddress}`);
  console.log(`   CompoundV3Adapter: ${baseUrl}/address/${compoundAdapterAddress}`);
  console.log(`   FlashLoanRebalancer: ${baseUrl}/address/${rebalancerAddress}`);

  console.log("\n🎉 Ready to prevent liquidations!\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Deployment failed:", error);
    process.exit(1);
  });
