const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("LiquidationPrevention", function () {
  let liquidationPrevention;
  let aaveAdapter;
  let compoundAdapter;
  let rebalancer;
  let owner;
  let user1;
  let user2;

  // Mock addresses for testing
  const MOCK_AAVE_POOL = "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951";
  const MOCK_COMPOUND_COMET = "0xAec1F48e02Cfb822Be958B68C7957156EB3F0b6e";
  const MOCK_ADDRESSES_PROVIDER = "0x0496275d34753A48320CA58103d5220d394FF77F";

  beforeEach(async function () {
    [owner, user1, user2] = await ethers.getSigners();

    // Deploy adapters
    const AaveV3Adapter = await ethers.getContractFactory("AaveV3Adapter");
    aaveAdapter = await AaveV3Adapter.deploy(MOCK_AAVE_POOL);
    await aaveAdapter.deployed();

    const CompoundV3Adapter = await ethers.getContractFactory("CompoundV3Adapter");
    compoundAdapter = await CompoundV3Adapter.deploy(MOCK_COMPOUND_COMET);
    await compoundAdapter.deployed();

    // Deploy rebalancer
    const FlashLoanRebalancer = await ethers.getContractFactory("FlashLoanRebalancer");
    rebalancer = await FlashLoanRebalancer.deploy(
      MOCK_ADDRESSES_PROVIDER,
      MOCK_AAVE_POOL,
      owner.address
    );
    await rebalancer.deployed();

    // Deploy main contract
    const LiquidationPrevention = await ethers.getContractFactory("LiquidationPrevention");
    liquidationPrevention = await LiquidationPrevention.deploy(
      aaveAdapter.address,
      compoundAdapter.address,
      rebalancer.address
    );
    await liquidationPrevention.deployed();
  });

  describe("Deployment", function () {
    it("Should set the correct adapters", async function () {
      expect(await liquidationPrevention.aaveAdapter()).to.equal(aaveAdapter.address);
      expect(await liquidationPrevention.compoundAdapter()).to.equal(compoundAdapter.address);
      expect(await liquidationPrevention.rebalancer()).to.equal(rebalancer.address);
    });

    it("Should grant admin role to deployer", async function () {
      const DEFAULT_ADMIN_ROLE = await liquidationPrevention.DEFAULT_ADMIN_ROLE();
      expect(await liquidationPrevention.hasRole(DEFAULT_ADMIN_ROLE, owner.address)).to.be.true;
    });

    it("Should start with zero registered users", async function () {
      expect(await liquidationPrevention.getRegisteredUsersCount()).to.equal(0);
    });
  });

  describe("User Registration", function () {
    it("Should allow user to register for Aave monitoring", async function () {
      await expect(
        liquidationPrevention.connect(user1).registerUser(true, false, ethers.utils.parseEther("1.5"))
      )
        .to.emit(liquidationPrevention, "UserRegistered")
        .withArgs(user1.address, true, false, ethers.utils.parseEther("1.5"), await getTimestamp());

      const config = await liquidationPrevention.getUserConfig(user1.address);
      expect(config.isRegistered).to.be.true;
      expect(config.monitorAave).to.be.true;
      expect(config.monitorCompound).to.be.false;
      expect(config.minHealthFactor).to.equal(ethers.utils.parseEther("1.5"));
    });

    it("Should allow user to register for both protocols", async function () {
      await liquidationPrevention.connect(user1).registerUser(true, true, ethers.utils.parseEther("2.0"));

      const config = await liquidationPrevention.getUserConfig(user1.address);
      expect(config.monitorAave).to.be.true;
      expect(config.monitorCompound).to.be.true;
    });

    it("Should reject registration with no protocols selected", async function () {
      await expect(
        liquidationPrevention.connect(user1).registerUser(false, false, ethers.utils.parseEther("1.5"))
      ).to.be.revertedWith("Must monitor at least one protocol");
    });

    it("Should reject registration with health factor too low", async function () {
      await expect(
        liquidationPrevention.connect(user1).registerUser(true, false, ethers.utils.parseEther("1.0"))
      ).to.be.revertedWith("Min health factor too low");
    });

    it("Should reject registration with health factor too high", async function () {
      await expect(
        liquidationPrevention.connect(user1).registerUser(true, false, ethers.utils.parseEther("4.0"))
      ).to.be.revertedWith("Min health factor too high");
    });

    it("Should reject duplicate registration", async function () {
      await liquidationPrevention.connect(user1).registerUser(true, false, ethers.utils.parseEther("1.5"));
      
      await expect(
        liquidationPrevention.connect(user1).registerUser(true, false, ethers.utils.parseEther("1.5"))
      ).to.be.revertedWith("Already registered");
    });

    it("Should increment registered users count", async function () {
      await liquidationPrevention.connect(user1).registerUser(true, false, ethers.utils.parseEther("1.5"));
      expect(await liquidationPrevention.getRegisteredUsersCount()).to.equal(1);

      await liquidationPrevention.connect(user2).registerUser(true, true, ethers.utils.parseEther("2.0"));
      expect(await liquidationPrevention.getRegisteredUsersCount()).to.equal(2);
    });
  });

  describe("User Configuration Updates", function () {
    beforeEach(async function () {
      await liquidationPrevention.connect(user1).registerUser(true, false, ethers.utils.parseEther("1.5"));
    });

    it("Should allow user to update configuration", async function () {
      await expect(
        liquidationPrevention.connect(user1).updateUserConfig(true, true, ethers.utils.parseEther("2.0"))
      )
        .to.emit(liquidationPrevention, "UserConfigUpdated")
        .withArgs(user1.address, true, true, ethers.utils.parseEther("2.0"), await getTimestamp());

      const config = await liquidationPrevention.getUserConfig(user1.address);
      expect(config.monitorCompound).to.be.true;
      expect(config.minHealthFactor).to.equal(ethers.utils.parseEther("2.0"));
    });

    it("Should reject update from unregistered user", async function () {
      await expect(
        liquidationPrevention.connect(user2).updateUserConfig(true, false, ethers.utils.parseEther("1.5"))
      ).to.be.revertedWith("Not registered");
    });
  });

  describe("User Unregistration", function () {
    beforeEach(async function () {
      await liquidationPrevention.connect(user1).registerUser(true, false, ethers.utils.parseEther("1.5"));
    });

    it("Should allow user to unregister", async function () {
      await expect(liquidationPrevention.connect(user1).unregisterUser())
        .to.emit(liquidationPrevention, "UserUnregistered")
        .withArgs(user1.address, await getTimestamp());

      const config = await liquidationPrevention.getUserConfig(user1.address);
      expect(config.isRegistered).to.be.false;
    });

    it("Should reject unregistration from non-registered user", async function () {
      await expect(
        liquidationPrevention.connect(user2).unregisterUser()
      ).to.be.revertedWith("Not registered");
    });
  });

  describe("Role-Based Access Control", function () {
    it("Should allow admin to grant monitor role", async function () {
      const MONITOR_ROLE = await liquidationPrevention.MONITOR_ROLE();
      await liquidationPrevention.grantRole(MONITOR_ROLE, user1.address);
      
      expect(await liquidationPrevention.hasRole(MONITOR_ROLE, user1.address)).to.be.true;
    });

    it("Should allow admin to grant agent role", async function () {
      const AGENT_ROLE = await liquidationPrevention.AGENT_ROLE();
      await liquidationPrevention.grantRole(AGENT_ROLE, user1.address);
      
      expect(await liquidationPrevention.hasRole(AGENT_ROLE, user1.address)).to.be.true;
    });
  });

  describe("Pause Functionality", function () {
    it("Should allow admin to pause contract", async function () {
      await liquidationPrevention.pause();
      expect(await liquidationPrevention.paused()).to.be.true;
    });

    it("Should prevent registration when paused", async function () {
      await liquidationPrevention.pause();
      
      await expect(
        liquidationPrevention.connect(user1).registerUser(true, false, ethers.utils.parseEther("1.5"))
      ).to.be.revertedWith("Pausable: paused");
    });

    it("Should allow admin to unpause contract", async function () {
      await liquidationPrevention.pause();
      await liquidationPrevention.unpause();
      
      expect(await liquidationPrevention.paused()).to.be.false;
    });

    it("Should reject pause from non-admin", async function () {
      await expect(
        liquidationPrevention.connect(user1).pause()
      ).to.be.reverted;
    });
  });

  describe("Statistics", function () {
    it("Should return initial stats as zero", async function () {
      const stats = await liquidationPrevention.getStats();
      expect(stats.totalMonitored).to.equal(0);
      expect(stats.risksDetected).to.equal(0);
      expect(stats.rebalancesExecuted).to.equal(0);
      expect(stats.liquidationsPrevented).to.equal(0);
    });
  });

  // Helper function to get current block timestamp
  async function getTimestamp() {
    const blockNum = await ethers.provider.getBlockNumber();
    const block = await ethers.provider.getBlock(blockNum);
    return block.timestamp;
  }
});
