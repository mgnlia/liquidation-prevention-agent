const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying Liquidation Prevention Agent...");
  console.log("Network:", hre.network.name);

  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  console.log("Account balance:", (await deployer.provider.getBalance(deployer.address)).toString());

  // Network-specific addresses
  const networkAddresses = {
    sepolia: {
      aavePoolAddressProvider: "0x0496275d34753A48320CA58103d5220d394FF77F",
      aavePool: "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951",
    },
    baseSepolia: {
      aavePoolAddressProvider: "0x0496275d34753A48320CA58103d5220d394FF77F", // Update with actual Base addresses
      aavePool: "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951",
    },
    arbitrumSepolia: {
      aavePoolAddressProvider: "0x0496275d34753A48320CA58103d5220d394FF77F", // Update with actual Arbitrum addresses
      aavePool: "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951",
    }
  };

  const addresses = networkAddresses[hre.network.name];
  if (!addresses) {
    throw new Error(`No addresses configured for network: ${hre.network.name}`);
  }

  // 1. Deploy Aave Adapter
  console.log("\n📦 Deploying AaveAdapter...");
  const AaveAdapter = await hre.ethers.getContractFactory("AaveAdapter");
  const aaveAdapter = await AaveAdapter.deploy(addresses.aavePoolAddressProvider);
  await aaveAdapter.waitForDeployment();
  const aaveAdapterAddress = await aaveAdapter.getAddress();
  console.log("✅ AaveAdapter deployed to:", aaveAdapterAddress);

  // 2. Deploy Compound Adapter (placeholder for now)
  console.log("\n📦 Deploying CompoundAdapter...");
  const CompoundAdapter = await hre.ethers.getContractFactory("CompoundAdapter");
  const compoundAdapter = await CompoundAdapter.deploy(
    "0x0000000000000000000000000000000000000000" // Placeholder - update with actual Comet address
  );
  await compoundAdapter.waitForDeployment();
  const compoundAdapterAddress = await compoundAdapter.getAddress();
  console.log("✅ CompoundAdapter deployed to:", compoundAdapterAddress);

  // 3. Deploy Flash Loan Rebalancer
  console.log("\n📦 Deploying FlashLoanRebalancer...");
  const FlashLoanRebalancer = await hre.ethers.getContractFactory("FlashLoanRebalancer");
  const flashLoanRebalancer = await FlashLoanRebalancer.deploy(
    addresses.aavePool,
    aaveAdapterAddress,
    compoundAdapterAddress
  );
  await flashLoanRebalancer.waitForDeployment();
  const flashLoanRebalancerAddress = await flashLoanRebalancer.getAddress();
  console.log("✅ FlashLoanRebalancer deployed to:", flashLoanRebalancerAddress);

  // 4. Deploy Main LiquidationPrevention Contract
  console.log("\n📦 Deploying LiquidationPrevention...");
  const LiquidationPrevention = await hre.ethers.getContractFactory("LiquidationPrevention");
  const liquidationPrevention = await LiquidationPrevention.deploy(
    aaveAdapterAddress,
    compoundAdapterAddress,
    flashLoanRebalancerAddress
  );
  await liquidationPrevention.waitForDeployment();
  const liquidationPreventionAddress = await liquidationPrevention.getAddress();
  console.log("✅ LiquidationPrevention deployed to:", liquidationPreventionAddress);

  // 5. Configure permissions
  console.log("\n🔧 Configuring permissions...");
  
  // Set LiquidationPrevention as authorized caller on FlashLoanRebalancer
  const tx1 = await flashLoanRebalancer.setAuthorizedCaller(liquidationPreventionAddress, true);
  await tx1.wait();
  console.log("✅ Authorized LiquidationPrevention on FlashLoanRebalancer");

  // Summary
  console.log("\n" + "=".repeat(60));
  console.log("🎉 Deployment Complete!");
  console.log("=".repeat(60));
  console.log("\nContract Addresses:");
  console.log("-------------------");
  console.log("AaveAdapter:           ", aaveAdapterAddress);
  console.log("CompoundAdapter:       ", compoundAdapterAddress);
  console.log("FlashLoanRebalancer:   ", flashLoanRebalancerAddress);
  console.log("LiquidationPrevention: ", liquidationPreventionAddress);
  console.log("\n📝 Update your .env file with these addresses:");
  console.log(`LIQUIDATION_PREVENTION_ADDRESS=${liquidationPreventionAddress}`);
  console.log(`AAVE_ADAPTER_ADDRESS=${aaveAdapterAddress}`);
  console.log(`COMPOUND_ADAPTER_ADDRESS=${compoundAdapterAddress}`);
  console.log(`FLASH_LOAN_REBALANCER_ADDRESS=${flashLoanRebalancerAddress}`);
  
  // Verification commands
  console.log("\n🔍 Verify contracts with:");
  console.log(`npx hardhat verify --network ${hre.network.name} ${aaveAdapterAddress} ${addresses.aavePoolAddressProvider}`);
  console.log(`npx hardhat verify --network ${hre.network.name} ${compoundAdapterAddress} 0x0000000000000000000000000000000000000000`);
  console.log(`npx hardhat verify --network ${hre.network.name} ${flashLoanRebalancerAddress} ${addresses.aavePool} ${aaveAdapterAddress} ${compoundAdapterAddress}`);
  console.log(`npx hardhat verify --network ${hre.network.name} ${liquidationPreventionAddress} ${aaveAdapterAddress} ${compoundAdapterAddress} ${flashLoanRebalancerAddress}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
