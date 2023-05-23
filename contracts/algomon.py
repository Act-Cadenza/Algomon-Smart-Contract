from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():
    localPlayerHp = Bytes('player_hp')
    localDmg = Bytes('player_dmg')

    localMonsHp = Bytes('mons_hp')
    localMonsDmg = Bytes('mons_dmg')

    localScore = Bytes('capturedScore')
    localTotal = Bytes('Total')

    # global
    globalScore = Bytes('globalScore')

    # void call
    opPlayerAttack = Bytes('attack_mons')
    opRun = Bytes('run')
    opCatch = Bytes('captured')
    opRevive = Bytes('revive')
    opProceed = Bytes('proceed')

    # boolean
    isInBattle = Bytes('isinBattle')
    isCaught = Bytes('isCaught')
    isBattleOver = Bytes('isBattleOver')
    isGameOver = Bytes('isGameOver')
    isButtonDisabled = Bytes('isButtonDisabled')

    scratchPlayerHp = ScratchVar(TealType.uint64)
    scratchPLayerAttack = ScratchVar(TealType.uint64)
    scratchMonsHp = ScratchVar(TealType.uint64)
    scratchMonsAttack = ScratchVar(TealType.uint64)

    scratchScore = ScratchVar(TealType.uint64)
    scratchglobalScore = ScratchVar(TealType.uint64)

    @Subroutine(TealType.none)
    def attack():
        return Seq(
            # basic sanity checks
            program.check_self(
                group_size=Int(1),
                group_index=Int(0),
            ),
            program.check_rekey_zero(1),
            Assert(
                And(
                    App.localGet(Int(0), localMonsHp) > Int(0),
                    App.localGet(Int(0), localPlayerHp) > Int(0),
                )
            ),
            scratchMonsHp.store(App.localGet(Int(0), localMonsHp)),
            scratchMonsAttack.store(App.localGet(Int(0), localMonsDmg)),
            scratchPlayerHp.store(App.localGet(Int(0), localPlayerHp)),
            scratchPLayerAttack.store(App.localGet(Int(0), localDmg)),

            If(Gt(scratchPlayerHp.load(), scratchMonsAttack.load()))
            .Then(
                App.localPut(Int(0), localPlayerHp,
                             scratchPlayerHp.load() - (scratchMonsAttack.load())),
            )
            .Else(
                Seq(
                    App.localPut(Int(0), localPlayerHp, Int(0)),
                    App.localPut(Int(0), isGameOver, Int(1)),

                )
            ),

            If(Gt(scratchMonsHp.load(), scratchPLayerAttack.load()))
            .Then(
                App.localPut(Int(0), localMonsHp, scratchMonsHp.load() - \
                             (scratchPLayerAttack.load())),
            )
            .Else(
                Seq(
                    App.localPut(Int(0), localMonsHp, Int(0)),
                    App.localPut(Int(0), isBattleOver, Int(1)),
                )
            ),

            Approve(),
        )

    @ Subroutine(TealType.none)
    def revive():
        return Seq(
            # basic sanity checks
            program.check_self(
                group_size=Int(1),
                group_index=Int(0),
            ),
            program.check_rekey_zero(1),

            App.localPut(Int(0), localPlayerHp, Int(100)),
            App.localPut(Int(0), localMonsHp, Int(50)),
            App.localPut(Int(0), isCaught, Int(0)),
            App.localPut(Int(0), isBattleOver, Int(0)),
            App.localPut(Int(0), isInBattle, Int(0)),
            App.localPut(Int(0), isButtonDisabled, Int(0)),
            App.localPut(Int(0), isGameOver, Int(0)),
            App.localPut(Int(0), localTotal, App.globalGet(
                globalScore)),
            Approve(),
        )

    @ Subroutine(TealType.none)
    def capture():
        return Seq(
            # basic sanity checks
            program.check_self(
                group_size=Int(1),
                group_index=Int(0),
            ),
            program.check_rekey_zero(1),
            Assert(
                And(
                    App.localGet(Int(0), localMonsHp) > Int(0),
                    App.localGet(Int(0), localPlayerHp) > Int(0),
                )
            ),
            scratchScore.store(App.localGet(Int(0), localScore)),
            scratchglobalScore.store(App.globalGet(globalScore)),
            App.localPut(Int(0), localScore, scratchScore.load() + Int(1)),
            App.globalPut(globalScore,
                          scratchglobalScore.load() + Int(1)),
            App.localPut(Int(0), isInBattle, Int(0)),
            App.localPut(Int(0), localMonsHp, Int(50)),
            App.localPut(Int(0), isCaught, Int(1)),
            Approve(),
        )

    @ Subroutine(TealType.none)
    def handleclick():
        return Seq(
            # basic sanity checks
            program.check_self(
                group_size=Int(1),
                group_index=Int(0),
            ),
            program.check_rekey_zero(1),

            App.localPut(Int(0), isButtonDisabled, Int(1)),
            App.localPut(Int(0), isInBattle, Int(1)),
            App.localPut(Int(0), localTotal, App.globalGet(
                globalScore)),
            Approve(),
        )

    @ Subroutine(TealType.none)
    def backmap():
        return Seq(
            # basic sanity checks
            program.check_self(
                group_size=Int(1),
                group_index=Int(0),
            ),
            program.check_rekey_zero(1),

            App.localPut(Int(0), isCaught, Int(0)),
            App.localPut(Int(0), isBattleOver, Int(0)),
            App.localPut(Int(0), isInBattle, Int(0)),
            App.localPut(Int(0), localMonsHp, Int(50)),
            App.localPut(Int(0), isButtonDisabled, Int(0)),
            App.localPut(Int(0), localTotal, App.globalGet(
                globalScore)),
            Approve(),
        )

    return program.event(
        init=Seq(
            App.globalPut(globalScore, Int(0)),
            Approve(),
        ),
        opt_in=Seq(
            App.localPut(Int(0), localPlayerHp, Int(100)),
            App.localPut(Int(0), localDmg, Int(20)),
            App.localPut(Int(0), localMonsHp, Int(50)),
            App.localPut(Int(0), localMonsDmg, Int(14)),
            App.localPut(Int(0), localScore, Int(0)),
            App.localPut(Int(0), isInBattle, Int(0)),
            App.localPut(Int(0), isCaught, Int(0)),
            App.localPut(Int(0), isBattleOver, Int(0)),
            App.localPut(Int(0), isGameOver, Int(0)),
            App.localPut(Int(0), isButtonDisabled, Int(0)),
            App.localPut(Int(0), localTotal, Int(0)),
            Approve(),
        ),
        no_op=Seq(
            Cond(
                [
                    Txn.application_args[0] == opPlayerAttack,
                    attack(),

                ],
                [
                    Txn.application_args[0] == opRun,
                    backmap(),

                ],
                [
                    Txn.application_args[0] == opCatch,
                    capture(),

                ],
                [
                    Txn.application_args[0] == opRevive,
                    revive(),

                ],
                [
                    Txn.application_args[0] == opProceed,
                    handleclick(),

                ],

            ),
            Reject(),
        ),
    )


def clear():
    return Approve()
