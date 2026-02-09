const hre = require("hardhat");

// Sepolia testnet addresses for Aave V3
const SEPOLIA_ADDRESSES = {
  aavePoolAddressesProvider: "0x012bAC54348C0E635dCAc9D5FB99f06F24136C9A",
  aavePool: "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951",
  compoundComet: "0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e", // USDC Comet on Sepolia
};

// Base Sepolia addresses
const BASE_SEPOLIA_ADDRESSES = {
  aavePoolAddressesProvider: "0x0000000000000000000000000000000000000000", // Update when available
  aavePool: "0x0000000000000000000000000000000000000000",
  compoundComet: "0x0000000000000000000000000000000000000000",
};

// Arbitrum Sepolia addresses
const ARBITRUM_SEPOLIA_ADDRESSES = {
  aavePoolAddressesProvider: "0x0000000000000000000000000000000000000000", // Update when available
  aavePool: "0x0000000000000000000000000000000000000000",
  compoundComet: "0x0000000000000000000000000000000000000000",
};

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  const network = hre.network.name;

  console.log("Deploying contracts with account:", deployer.address);
  console.log("Network:", network);
  console.log("Account balance:", (await hre.ethers.provider.getBalance(deployer.address)).toString());

  // Select addresses based on network
  let addresses;
  if (network === "sepolia") {
    addresses = SEPOLIA_ADDRESSES;
  } else if (network === "baseSepolia") {
    addresses = BASE_SEPOLIA_ADDRESSES;
  } else if (network === "arbitrumSepolia") {
    addresses = ARBITRUM_SEPOLIA_ADDRESSES;
  } else {
    console.log("Using Sepolia addresses for local/hardhat network");
    addresses = SEPOLIA_ADDRESSES;
  }

  // Deploy AaveAdapter
  console.log("\n1. Deploying AaveAdapter...");
  const AaveAdapter = await hre.ethers.getContractFactory("AaveAdapter");
  const aaveAdapter = await AaveAdapter.deploy(addresses.aavePoolAddressesProvider);
  await aaveAdapter.waitForDeployment();
  const aaveAdapterAddress = await aaveAdapter.getAddress();
  console.log("AaveAdapter deployed to:", aaveAdapterAddress);

  // Deploy CompoundAdapter
  console.log("\n2. Deploying CompoundAdapter...");
  const CompoundAdapter = await hre.ethers.getContractFactory("CompoundAdapter");
  const compoundAdapter = await CompoundAdapter.deploy(addresses.compoundComet);
  await compoundAdapter.waitForDeployment();
  const compoundAdapterAddress = await compoundAdapter.getAddress();
  console.log("CompoundAdapter deployed to:", compoundAdapterAddress);

  // Deploy FlashLoanRebalancer
  console.log("\n3. Deploying FlashLoanRebalancer...");
  const FlashLoanRebalancer = await hre.ethers.getContractFactory("FlashLoanRebalancer");
  const flashLoanRebalancer = await FlashLoanRebalancer.deploy(addresses.aavePool);
  await flashLoanRebalancer.waitForDeployment();
  const flashLoanRebalancerAddress = await flashLoanRebalancer.getAddress();
  console.log("FlashLoanRebalancer deployed to:", flashLoanRebalancerAddress);

  // Deploy LiquidationPrevention
  console.log("\n4. Deploying LiquidationPrevention...");
  const LiquidationPrevention = await hre.ethers.getContractFactory("LiquidationPrevention");
  const liquidationPrevention = await LiquidationPrevention.deploy(
    aaveAdapterAddress,
    compoundAdapterAddress,
    flashLoanRebalancerAddress
  );
  await liquidationPrevention.waitForDeployment();
  const liquidationPreventionAddress = await liquidationPrevention.getAddress();
  console.log("LiquidationPrevention deployed to:", liquidationPreventionAddress);

  // Set LiquidationPrevention address in FlashLoanRebalancer
  console.log("\n5. Configuring FlashLoanRebalancer...");
  const tx = await flashLoanRebalancer.setLiquidationPrevention(liquidationPreventionAddress);
  await tx.wait();
  console.log("FlashLoanRebalancer configured");

  console.log("\n=== DEPLOYMENT SUMMARY ===");
  console.log("Network:", network);
  console.log("AaveAdapter:", aaveAdapterAddress);
  console.log("CompoundAdapter:", compoundAdapterAddress);
  console.log("FlashLoanRebalancer:", flashLoanRebalancerAddress);
  console.log("LiquidationPrevention:", liquidationPreventionAddress);

  console.log("\n=== VERIFICATION COMMANDS ===");
  console.log(`npx hardhat verify --network ${network} ${aaveAdapterAddress} ${addresses.aavePoolAddressesProvider}`);
  console.log(`npx hardhat verify --network ${network} ${compoundAdapterAddress} ${addresses.compoundComet}`);
  console.log(`npx hardhat verify --network ${network} ${flashLoanRebalancerAddress} ${addresses.aavePool}`);
  console.log(`npx hardhat verify --network ${network} ${liquidationPreventionAddress} ${aaveAdapterAddress} ${compoundAdapterAddress} ${flashLoanRebalancerAddress}`);

  // Save deployment addresses
  const fs = require("fs");
  const deploymentInfo = {
    network,
    timestamp: new Date().toISOString(),
    contracts: {
      AaveAdapter: aaveAdapterAddress,
      CompoundAdapter: compoundAdapterAddress,
      FlashLoanRebalancer: flashLoanRebalancerAddress,
      LiquidationPrevention: liquidationPreventionAddress,
    },
    protocolAddresses: addresses,
  };

  fs.writeFileSync(
    `deployments/${network}-${Date.now()}.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("\nDeployment info saved to deployments/");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
