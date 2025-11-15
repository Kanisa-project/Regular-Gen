class Chest(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.chests
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, "closed_chest.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.opened = False
        if self.game.player.occupation == "knight":
            self.full_item_list = ["apple","bread"]
        if self.game.player.occupation == "hunter":
            self.full_item_list = ["apple","bread"]
        if self.game.player.occupation == "mage":
            self.full_item_list = ["apple","bread","water","milk"]
        self.num_of_items = random.randint(1,5)
        self.item_list = []
        for i in range(self.num_of_items):
            self.item_list += [self.full_item_list[random.randint(0,len(self.full_item_list)-1)]]
    def update(self):
        if self.opened:
            self.image = pg.image.load(os.path.join(img_folder, "opened_chest.png")).convert()
        else:
            self.image = pg.image.load(os.path.join(img_folder, "closed_chest.png")).convert()
        
    def open_chest(self,player):
        self.opened = True
        player.coinbag += 10 * player.vfdscore[1]
        for item in self.item_list:
            if item == "apple" and player.carried_weight < player.weight_limit:
                player.backpack += [Apple(self.game,8,11)]
				player.move_speed -= 1
            if item == "bread" and player.carried_weight < player.weight_limit:
                player.backpack += [Bread(self.game,8,11)]
				player.move_speed -= 1
            if item == "milk" and player.carried_weight < player.weight_limit:
                player.backpack += [Milk(self.game,8,11)]
				player.move_speed -= 1
            if item == "water" and player.carried_weight < player.weight_limit:
                player.backpack += [Water(self.game,8,11)]
				player.move_speed -= 1
        self.kill()