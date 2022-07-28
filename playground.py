import smartpy as sp

class Playground (sp.Contract):
    def __init__(self):
    #storage
        self.init(
            num_1 = sp.nat(5),
            num_2 = sp.int(-2),
            admin = sp.test_account("admin").address,
            time = sp.timestamp(25),
            map_1 = sp.map(l={} , tkey =sp.TNat  , tvalue = sp.TAddress),
            map_2 = sp.big_map(l={},tkey=sp.TNat,tvalue=sp.TAddress),
        )
    @sp.entry_point
    def change_num_values(self,params):
        sp.set_type(params,sp.TRecord(num_a= sp.TNat,num_b=sp.TInt))

        #Assertions
        sp.verify(sp.sender == self.data.admin,"NOT AUTHORISED")
        sp.verify(sp.now> self.data.time,"INCORRECT TIMING")

        #Assignment
        self.data.num_1 = params.num_a

        #Conditional 
        sp.if params.num_b > 0:
            self.data.num_2 = params.num_b
        sp.else:
            self.data.num_2 = -1 * params.num_b

    @sp.entry_point
    def change_map_value(self,num):
        sp.set_type(num,sp.TNat)

        self.data.map_1[num] = sp.sender
        self.data.map_2[num] = sp.sender


@sp.add_test(name="main")
def test():
    scenario = sp.test_scenario()

    #Testing accounts
    alice = sp.test_account("alice")
    bob = sp.test_account("bob")
    admin =sp.test_account("admin")

    playground = Playground()

    #Important
    scenario +=playground
    #call change_num_values
    scenario += playground.change_num_values(num_a=sp.nat(2),num_b=sp.int(-3)).run(
        sender=admin,now=sp.timestamp(26)
    )
    #call change_map_values
    scenario += playground.change_map_value(5).run(sender=alice)
    
    #invalid responce to get reverted transaction
    scenario += playground.change_num_values(num_a=sp.nat(2),num_b=sp.int(-3)).run(
        sender=alice,now=sp.timestamp(26),valid=False
    )
    
