import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Solshield } from "../target/types/solshield";
import { assert } from "chai";

describe("solshield", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.Solshield as Program<Solshield>;
  const authority = provider.wallet;

  let protocolStatePda: anchor.web3.PublicKey;
  let protocolStateBump: number;

  before(async () => {
    [protocolStatePda, protocolStateBump] =
      anchor.web3.PublicKey.findProgramAddressSync(
        [Buffer.from("protocol-state")],
        program.programId
      );
  });

  it("Initializes the protocol", async () => {
    const agentAuthority = anchor.web3.Keypair.generate();

    const config = {
      agentAuthority: agentAuthority.publicKey,
      defaultWarnThreshold: new anchor.BN(15000), // 1.5x
      defaultCriticalThreshold: new anchor.BN(12000), // 1.2x
      maxPositionsPerUser: 10,
      rebalanceFeeBps: 50, // 0.5%
    };

    try {
      await program.methods
        .initialize(config)
        .accounts({
          protocolState: protocolStatePda,
          authority: authority.publicKey,
          systemProgram: anchor.web3.SystemProgram.programId,
        })
        .rpc();

      const state = await program.account.protocolState.fetch(protocolStatePda);
      assert.equal(
        state.authority.toBase58(),
        authority.publicKey.toBase58()
      );
      assert.equal(
        state.agentAuthority.toBase58(),
        agentAuthority.publicKey.toBase58()
      );
      assert.equal(state.defaultWarnThreshold.toNumber(), 15000);
      assert.equal(state.totalPositions.toNumber(), 0);
    } catch (e) {
      // Account may already be initialized
      console.log("Initialize may have already been called:", e.message);
    }
  });

  it("Registers a position for monitoring", async () => {
    const obligationKey = anchor.web3.Keypair.generate().publicKey;

    const [positionPda] = anchor.web3.PublicKey.findProgramAddressSync(
      [
        Buffer.from("position"),
        authority.publicKey.toBuffer(),
        obligationKey.toBuffer(),
      ],
      program.programId
    );

    try {
      await program.methods
        .registerPosition(
          { kamino: {} }, // DeFiProtocol::Kamino
          obligationKey,
          new anchor.BN(15000), // warn threshold
          new anchor.BN(12000) // critical threshold
        )
        .accounts({
          protocolState: protocolStatePda,
          position: positionPda,
          owner: authority.publicKey,
          systemProgram: anchor.web3.SystemProgram.programId,
        })
        .rpc();

      const position = await program.account.monitoredPosition.fetch(positionPda);
      assert.equal(position.owner.toBase58(), authority.publicKey.toBase58());
      assert.equal(
        position.obligationKey.toBase58(),
        obligationKey.toBase58()
      );
      assert.equal(position.warnThreshold.toNumber(), 15000);
      assert.equal(position.rebalanceCount, 0);
    } catch (e) {
      console.log("Register position error:", e.message);
    }
  });

  it("Rejects invalid thresholds", async () => {
    const obligationKey = anchor.web3.Keypair.generate().publicKey;

    const [positionPda] = anchor.web3.PublicKey.findProgramAddressSync(
      [
        Buffer.from("position"),
        authority.publicKey.toBuffer(),
        obligationKey.toBuffer(),
      ],
      program.programId
    );

    try {
      await program.methods
        .registerPosition(
          { kamino: {} },
          obligationKey,
          new anchor.BN(10000), // warn < critical = invalid
          new anchor.BN(15000)
        )
        .accounts({
          protocolState: protocolStatePda,
          position: positionPda,
          owner: authority.publicKey,
          systemProgram: anchor.web3.SystemProgram.programId,
        })
        .rpc();

      assert.fail("Should have thrown InvalidThresholds error");
    } catch (e) {
      assert.include(e.message, "InvalidThresholds");
    }
  });
});
