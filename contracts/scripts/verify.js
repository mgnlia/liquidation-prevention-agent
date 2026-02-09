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
  // Load latest deployment
  const deploymentsDir = path.join(__dirname, "../deployments");
  const files = fs.readdirSync(deploymentsDir)
    .filter(f => f.startsWith("sepolia-"))
    .sort()
    .reverse();
  
  if (files.length === 0) {
    console.error("❌ No deployment found. Deploy contracts first.");
    process.exit(1);
  }

  const latestDeployment = JSON.parse(
    fs.readFileSync(path.join(deploymentsDir, files[0]), "utf8")
  );

  console.log("🔍 Verifying contracts on Etherscan...\n");
  console.log("Using deployment from:", files[0], "\n");

  const { contracts } = latestDeployment;

  // Verify AaveV3Adapter
  console.log("Verifying AaveV3Adapter...");
  try {
    await hre.run("verify:verify", {
      address: contracts.aaveAdapter,
      constructorArguments: [SEPOLIA_ADDRESSES.AAVE_POOL],
    });
    console.log("✅ AaveV3Adapter verified\n");
  } catch (error) {
    console.log("⚠️  AaveV3Adapter:", error.message, "\n");
  }

  // Verify CompoundV3Adapter
  console.log("Verifying CompoundV3Adapter...");
  try {
    await hre.run("verify:verify", {
      address: contracts.compoundAdapter,
      constructorArguments: [SEPOLIA_ADDRESSES.COMPOUND_COMET_USDC],
    });
    console.log("✅ CompoundV3Adapter verified\n");
  } catch (error) {
    console.log("⚠️  CompoundV3Adapter:", error.message, "\n");
  }

  // Verify FlashLoanRebalancer
  console.log("Verifying FlashLoanRebalancer...");
  try {
    await hre.run("verify:verify", {
      address: contracts.rebalancer,
      constructorArguments: [
        SEPOLIA_ADDRESSES.AAVE_POOL_ADDRESSES_PROVIDER,
        SEPOLIA_ADDRESSES.AAVE_POOL,
        latestDeployment.deployer,
      ],
    });
    console.log("✅ FlashLoanRebalancer verified\n");
  } catch (error) {
    console.log("⚠️  FlashLoanRebalancer:", error.message, "\n");
  }

  // Verify LiquidationPrevention
  console.log("Verifying LiquidationPrevention...");
  try {
    await hre.run("verify:verify", {
      address: contracts.liquidationPrevention,
      constructorArguments: [
        contracts.aaveAdapter,
        contracts.compoundAdapter,
        contracts.rebalancer,
      ],
    });
    console.log("✅ LiquidationPrevention verified\n");
  } catch (error) {
    console.log("⚠️  LiquidationPrevention:", error.message, "\n");
  }

  console.log("🎉 Verification complete!");
  console.log("\nView on Etherscan:");
  console.log(`  AaveV3Adapter:         https://sepolia.etherscan.io/address/${contracts.aaveAdapter}`);
  console.log(`  CompoundV3Adapter:     https://sepolia.etherscan.io/address/${contracts.compoundAdapter}`);
  console.log(`  FlashLoanRebalancer:   https://sepolia.etherscan.io/address/${contracts.rebalancer}`);
  console.log(`  LiquidationPrevention: https://sepolia.etherscan.io/address/${contracts.liquidationPrevention}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
