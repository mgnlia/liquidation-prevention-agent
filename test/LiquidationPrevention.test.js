const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("LiquidationPrevention", function () {
  let liquidationPrevention;
  let aaveAdapter;
  let compoundAdapter;
  let flashLoanRebalancer;
  let owner;
  let user;
  let agent;

  beforeEach(async function () {
    [owner, user, agent] = await ethers.getSigners();

    // Deploy mock adapters
    const AaveAdapter = await ethers.getContractFactory("AaveAdapter");
    aaveAdapter = await AaveAdapter.deploy(
      "0x0496275d34753A48320CA58103d5220d394FF77F" // Sepolia address
    );

    const CompoundAdapter = await ethers.getContractFactory("CompoundAdapter");
    compoundAdapter = await CompoundAdapter.deploy(
      ethers.ZeroAddress // Placeholder
    );

    // Deploy flash loan rebalancer
    const FlashLoanRebalancer = await ethers.getContractFactory("FlashLoanRebalancer");
    flashLoanRebalancer = await FlashLoanRebalancer.deploy(
      "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951", // Sepolia Aave pool
      await aaveAdapter.getAddress(),
      await compoundAdapter.getAddress()
    );

    // Deploy main contract
    const LiquidationPrevention = await ethers.getContractFactory("LiquidationPrevention");
    liquidationPrevention = await LiquidationPrevention.deploy(
      await aaveAdapter.getAddress(),
      await compoundAdapter.getAddress(),
      await flashLoanRebalancer.getAddress()
    );
  });

  describe("Deployment", function () {
    it("Should set the correct adapters", async function () {
      expect(await liquidationPrevention.aaveAdapter()).to.equal(await aaveAdapter.getAddress());
      expect(await liquidationPrevention.compoundAdapter()).to.equal(await compoundAdapter.getAddress());
    });

    it("Should set the owner correctly", async function () {
      expect(await liquidationPrevention.owner()).to.equal(owner.address);
    });
  });

  describe("User Configuration", function () {
    it("Should allow users to set configuration", async function () {
      const minHealthFactor = ethers.parseEther("1.5");
      const targetHealthFactor = ethers.parseEther("2.0");

      await liquidationPrevention.connect(user).setUserConfig(
        minHealthFactor,
        targetHealthFactor,
        true, // enableAave
        false // enableCompound
      );

      const config = await liquidationPrevention.userConfigs(user.address);
      expect(config.autoRebalanceEnabled).to.be.true;
      expect(config.minHealthFactor).to.equal(minHealthFactor);
      expect(config.targetHealthFactor).to.equal(targetHealthFactor);
      expect(config.aaveEnabled).to.be.true;
      expect(config.compoundEnabled).to.be.false;
    });

    it("Should reject invalid health factors", async function () {
      const minHealthFactor = ethers.parseEther("1.0"); // Too low
      const targetHealthFactor = ethers.parseEther("2.0");

      await expect(
        liquidationPrevention.connect(user).setUserConfig(
          minHealthFactor,
          targetHealthFactor,
          true,
          false
        )
      ).to.be.revertedWith("Min health factor too low");
    });

    it("Should reject target < min", async function () {
      const minHealthFactor = ethers.parseEther("2.0");
      const targetHealthFactor = ethers.parseEther("1.5"); // Less than min

      await expect(
        liquidationPrevention.connect(user).setUserConfig(
          minHealthFactor,
          targetHealthFactor,
          true,
          false
        )
      ).to.be.revertedWith("Target must be > min");
    });
  });

  describe("Agent Authorization", function () {
    it("Should allow owner to authorize agents", async function () {
      await liquidationPrevention.connect(owner).setAgentAuthorization(agent.address, true);
      expect(await liquidationPrevention.authorizedAgents(agent.address)).to.be.true;
    });

    it("Should allow owner to deauthorize agents", async function () {
      await liquidationPrevention.connect(owner).setAgentAuthorization(agent.address, true);
      await liquidationPrevention.connect(owner).setAgentAuthorization(agent.address, false);
      expect(await liquidationPrevention.authorizedAgents(agent.address)).to.be.false;
    });

    it("Should reject non-owner authorization attempts", async function () {
      await expect(
        liquidationPrevention.connect(user).setAgentAuthorization(agent.address, true)
      ).to.be.revertedWithCustomError(liquidationPrevention, "OwnableUnauthorizedAccount");
    });
  });

  describe("Auto-Rebalance Toggle", function () {
    beforeEach(async function () {
      await liquidationPrevention.connect(user).setUserConfig(
        ethers.parseEther("1.5"),
        ethers.parseEther("2.0"),
        true,
        false
      );
    });

    it("Should allow users to disable auto-rebalance", async function () {
      await liquidationPrevention.connect(user).toggleAutoRebalance(false);
      const config = await liquidationPrevention.userConfigs(user.address);
      expect(config.autoRebalanceEnabled).to.be.false;
    });

    it("Should allow users to re-enable auto-rebalance", async function () {
      await liquidationPrevention.connect(user).toggleAutoRebalance(false);
      await liquidationPrevention.connect(user).toggleAutoRebalance(true);
      const config = await liquidationPrevention.userConfigs(user.address);
      expect(config.autoRebalanceEnabled).to.be.true;
    });
  });

  describe("Health Factor Queries", function () {
    beforeEach(async function () {
      await liquidationPrevention.connect(user).setUserConfig(
        ethers.parseEther("1.5"),
        ethers.parseEther("2.0"),
        true,
        false
      );
    });

    it("Should return health factors for enabled protocols", async function () {
      // Note: This will return 0 in test environment without actual Aave positions
      const healthFactors = await liquidationPrevention.getUserHealthFactors(user.address);
      expect(healthFactors.aaveHealth).to.be.a("bigint");
      expect(healthFactors.compoundHealth).to.equal(0n); // Compound not enabled
    });
  });
});
