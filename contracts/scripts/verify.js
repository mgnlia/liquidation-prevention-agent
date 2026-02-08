const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

// Load latest deployment
function getLatestDeployment() {
  const deploymentsDir = path.join(__dirname, "../deployments");
  const files = fs.readdirSync(deploymentsDir).filter(f => f.startsWith("sepolia-"));
  
  if (files.length === 0) {
    throw new Error("No deployment files found");
  }
  
  const latestFile = files.sort().reverse()[0];
  const deployment = JSON.parse(
    fs.readFileSync(path.join(deploymentsDir, latestFile), "utf8")
  );
  
  return deployment;
}

async function main() {
  console.log("🔍 Starting contract verification on Etherscan...\n");

  const deployment = getLatestDeployment();
  const contracts = deployment.contracts;

  // Sepolia addresses for constructor args
  const SEPOLIA_ADDRESSES = {
    AAVE_POOL: "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951",
    AAVE_POOL_ADDRESSES_PROVIDER: "0x0496275d34753A48320CA58103d5220d394FF77F",
    COMPOUND_COMET_USDC: "0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e",
  };

  try {
    // Verify AaveV3Adapter
    console.log("📝 Verifying AaveV3Adapter...");
    await hre.run("verify:verify", {
      address: contracts.aaveAdapter,
      constructorArguments: [SEPOLIA_ADDRESSES.AAVE_POOL],
    });
    console.log("✅ AaveV3Adapter verified\n");
  } catch (error) {
    console.log("⚠️  AaveV3Adapter verification failed:", error.message, "\n");
  }

  try {
    // Verify CompoundV3Adapter
    console.log("📝 Verifying CompoundV3Adapter...");
    await hre.run("verify:verify", {
      address: contracts.compoundAdapter,
      constructorArguments: [SEPOLIA_ADDRESSES.COMPOUND_COMET_USDC],
    });
    console.log("✅ CompoundV3Adapter verified\n");
  } catch (error) {
    console.log("⚠️  CompoundV3Adapter verification failed:", error.message, "\n");
  }

  try {
    // Verify FlashLoanRebalancer
    console.log("📝 Verifying FlashLoanRebalancer...");
    await hre.run("verify:verify", {
      address: contracts.rebalancer,
      constructorArguments: [
        SEPOLIA_ADDRESSES.AAVE_POOL_ADDRESSES_PROVIDER,
        SEPOLIA_ADDRESSES.AAVE_POOL,
        deployment.deployer,
      ],
    });
    console.log("✅ FlashLoanRebalancer verified\n");
  } catch (error) {
    console.log("⚠️  FlashLoanRebalancer verification failed:", error.message, "\n");
  }

  try {
    // Verify LiquidationPrevention
    console.log("📝 Verifying LiquidationPrevention...");
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
    console.log("⚠️  LiquidationPrevention verification failed:", error.message, "\n");
  }

  console.log("🎉 Verification process complete!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
