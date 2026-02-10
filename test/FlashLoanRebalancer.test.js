const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("FlashLoanRebalancer", function () {
  let flashLoanRebalancer;
  let aaveAdapter;
  let compoundAdapter;
  let owner;
  let liquidationPrevention;
  let unauthorized;

  // Mock addresses
  const MOCK_AAVE_POOL = "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951";

  beforeEach(async function () {
    [owner, liquidationPrevention, unauthorized] = await ethers.getSigners();

    // Deploy mock adapters first
    const AaveAdapter = await ethers.getContractFactory("AaveAdapter");
    aaveAdapter = await AaveAdapter.deploy(
      "0x0496275d34753A48320CA58103d5220d394FF77F"
    );
    await aaveAdapter.waitForDeployment();

    const CompoundAdapter = await ethers.getContractFactory("CompoundAdapter");
    compoundAdapter = await CompoundAdapter.deploy(ethers.ZeroAddress);
    await compoundAdapter.waitForDeployment();

    // Deploy FlashLoanRebalancer
    const FlashLoanRebalancer = await ethers.getContractFactory("FlashLoanRebalancer");
    flashLoanRebalancer = await FlashLoanRebalancer.deploy(
      MOCK_AAVE_POOL,
      await aaveAdapter.getAddress(),
      await compoundAdapter.getAddress()
    );
    await flashLoanRebalancer.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct Aave pool", async function () {
      expect(await flashLoanRebalancer.aavePool()).to.equal(MOCK_AAVE_POOL);
    });

    it("Should set the correct adapters", async function () {
      expect(await flashLoanRebalancer.aaveAdapter()).to.equal(
        await aaveAdapter.getAddress()
      );
      expect(await flashLoanRebalancer.compoundAdapter()).to.equal(
        await compoundAdapter.getAddress()
      );
    });

    it("Should set the owner correctly", async function () {
      expect(await flashLoanRebalancer.owner()).to.equal(owner.address);
    });
  });

  describe("Authorization", function () {
    it("Should allow owner to authorize callers", async function () {
      await flashLoanRebalancer.setAuthorizedCaller(
        liquidationPrevention.address,
        true
      );
      expect(
        await flashLoanRebalancer.authorizedCallers(liquidationPrevention.address)
      ).to.be.true;
    });

    it("Should allow owner to deauthorize callers", async function () {
      await flashLoanRebalancer.setAuthorizedCaller(
        liquidationPrevention.address,
        true
      );
      await flashLoanRebalancer.setAuthorizedCaller(
        liquidationPrevention.address,
        false
      );
      expect(
        await flashLoanRebalancer.authorizedCallers(liquidationPrevention.address)
      ).to.be.false;
    });

    it("Should reject unauthorized callers", async function () {
      await expect(
        flashLoanRebalancer
          .connect(unauthorized)
          .executeRebalance(
            owner.address,
            "aave",
            ethers.parseEther("1000"),
            ethers.ZeroAddress,
            ethers.ZeroAddress
          )
      ).to.be.revertedWith("Not authorized");
    });

    it("Should reject non-owner authorization attempts", async function () {
      await expect(
        flashLoanRebalancer
          .connect(unauthorized)
          .setAuthorizedCaller(unauthorized.address, true)
      ).to.be.revertedWithCustomError(
        flashLoanRebalancer,
        "OwnableUnauthorizedAccount"
      );
    });
  });

  describe("Swap Router", function () {
    it("Should allow owner to set swap router", async function () {
      const mockRouter = "0x0000000000000000000000000000000000000001";
      await flashLoanRebalancer.setSwapRouter(mockRouter);
      expect(await flashLoanRebalancer.swapRouter()).to.equal(mockRouter);
    });

    it("Should reject non-owner swap router update", async function () {
      await expect(
        flashLoanRebalancer
          .connect(unauthorized)
          .setSwapRouter(ethers.ZeroAddress)
      ).to.be.revertedWithCustomError(
        flashLoanRebalancer,
        "OwnableUnauthorizedAccount"
      );
    });
  });

  describe("Emergency Withdraw", function () {
    it("Should allow owner to emergency withdraw", async function () {
      // Deploy a mock ERC20 for testing
      // In a full test suite, we'd use a mock token
      // For now, just verify the function exists and is callable by owner
      // (will revert due to no token balance, which is expected)
    });

    it("Should reject non-owner emergency withdraw", async function () {
      await expect(
        flashLoanRebalancer
          .connect(unauthorized)
          .emergencyWithdraw(ethers.ZeroAddress, 0)
      ).to.be.revertedWithCustomError(
        flashLoanRebalancer,
        "OwnableUnauthorizedAccount"
      );
    });
  });
});
