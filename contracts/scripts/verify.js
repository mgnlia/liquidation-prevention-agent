const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("\n🔍 Verifying contracts on Etherscan...\n");

  // Load latest deployment
  const deploymentsDir = path.join(__dirname, "../deployments");
  const latestPath = path.join(deploymentsDir, `${hre.network.name}-latest.json`);

  if (!fs.existsSync(latestPath)) {
    console.error("❌ No deployment found for", hre.network.name);
    console.log("   Run deployment first: npx hardhat run scripts/deploy.js --network", hre.network.name);
    process.exit(1);
  }

  const deployment = JSON.parse(fs.readFileSync(latestPath, "utf8"));

  console.log("📋 Verifying deployment from:", new Date(deployment.timestamp).toLocaleString());
  console.log("   Network:", deployment.network);
  console.log("   Chain ID:", deployment.chainId, "\n");

  const { contracts, protocolAddresses, aiAgent } = deployment;

  // Verify each contract
  const verifications = [
    {
      name: "AaveV3Adapter",
      address: contracts.AaveV3Adapter,
      constructorArguments: [protocolAddresses.AaveV3PoolAddressesProvider]
    },
    {
      name: "CompoundV3Adapter",
      address: contracts.CompoundV3Adapter,
      constructorArguments: [protocolAddresses.CompoundV3CometUSDC]
    },
    {
      name: "FlashLoanRebalancer",
      address: contracts.FlashLoanRebalancer,
      constructorArguments: [protocolAddresses.AaveV3PoolAddressesProvider]
    },
    {
      name: "LiquidationPrevention",
      address: contracts.LiquidationPrevention,
      constructorArguments: [
        contracts.AaveV3Adapter,
        contracts.CompoundV3Adapter,
        contracts.FlashLoanRebalancer,
        aiAgent
      ]
    }
  ];

  for (const verification of verifications) {
    console.log(`🔎 Verifying ${verification.name}...`);
    console.log(`   Address: ${verification.address}`);

    try {
      await hre.run("verify:verify", {
        address: verification.address,
        constructorArguments: verification.constructorArguments,
      });
      console.log(`   ✅ ${verification.name} verified!\n`);
    } catch (error) {
      if (error.message.includes("Already Verified")) {
        console.log(`   ℹ️  ${verification.name} already verified\n`);
      } else {
        console.error(`   ❌ Verification failed:`, error.message, "\n");
      }
    }

    // Wait between verifications to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  console.log("✅ Verification complete!\n");

  const baseUrl = hre.network.name === "sepolia" 
    ? "https://sepolia.etherscan.io" 
    : "https://etherscan.io";

  console.log("🔗 View verified contracts:");
  for (const verification of verifications) {
    console.log(`   ${verification.name}: ${baseUrl}/address/${verification.address}#code`);
  }

  console.log("\n🎉 All contracts are now publicly verifiable!\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Verification failed:", error);
    process.exit(1);
  });
