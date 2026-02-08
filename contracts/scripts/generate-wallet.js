const { ethers } = require("hardhat");

async function main() {
  // Generate a new random wallet
  const wallet = ethers.Wallet.createRandom();
  
  console.log("🔐 NEW SEPOLIA WALLET GENERATED");
  console.log("=" .repeat(60));
  console.log("Address:", wallet.address);
  console.log("Private Key:", wallet.privateKey);
  console.log("Mnemonic:", wallet.mnemonic.phrase);
  console.log("=" .repeat(60));
  console.log("\n⚠️  SAVE THIS INFORMATION SECURELY!");
  console.log("\n💰 Fund this wallet with Sepolia ETH:");
  console.log("   https://sepoliafaucet.com");
  console.log("   https://faucet.sepolia.dev");
  console.log("   https://www.alchemy.com/faucets/ethereum-sepolia");
  console.log("\n📝 Add to contracts/.env:");
  console.log(`PRIVATE_KEY=${wallet.privateKey}`);
  console.log(`SEPOLIA_RPC_URL=https://rpc.sepolia.org`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
