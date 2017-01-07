"""
Purpose: The CardEnum represents the available cards for player strategies
    , and the Deck Manager.
"""

from enum import IntEnum


class CardEnum(IntEnum):
    NoCard = -1
    WheatField = 0
    Ranch = 2
    Bakery = 3
    Cafe = 4
    ConvenienceStore = 5
    Forest = 6
    TVStation = 7  # Not presently supported
    Stadium = 8  # Not presently supported
    BusinessCenter = 9  # Not presently supported
    CheeseFactory = 10
    FurnitureFactory = 11
    Mine = 12
    FamilyRestaurant = 13
    AppleOrchard = 14
    FruitAndVegetableStand = 15
# These are the major improvements
    TrainStation = 91
    ShoppingMall = 92
    AmusementPark = 93
    RadioTower = 94


"""Card Costs and types of cards are common knowledge to all elements"""
CardCosts = {
    CardEnum.WheatField: 1,
    CardEnum.Ranch: 1,
    CardEnum.Bakery: 1,
    CardEnum.Cafe: 2,
    CardEnum.ConvenienceStore: 2,
    CardEnum.Forest: 3,
    CardEnum.TVStation: 7,
    CardEnum.Stadium: 6,
    CardEnum.BusinessCenter: 8,
    CardEnum.CheeseFactory: 5,
    CardEnum.FurnitureFactory: 3,
    CardEnum.Mine: 6,
    CardEnum.FamilyRestaurant: 3,
    CardEnum.AppleOrchard: 3,
    CardEnum.FruitAndVegetableStand: 2,
# These are the major improvements
    CardEnum.TrainStation: 4,
    CardEnum.ShoppingMall: 10,
    CardEnum.AmusementPark: 16,
    CardEnum.RadioTower: 22
}
