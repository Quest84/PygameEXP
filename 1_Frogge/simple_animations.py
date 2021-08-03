def load_anims(anim_name, path, frames):
    anims = []
    for i in range(len(frames)):
        anims.append([path + anim_name + "_" + str(i) + ".png", frames[i]])
        print(anims[i])
    return anims 

class Ninja():
    def __init__(self):
        self.moving_right = False
        self.moving_left = False
        self.yvel = 0
        self.measurements = [53, 79]
        self.movement = [0, 0]
        self.airtimer = 0
        self.rect = pygame.Rect(50, 50, self.measurements[0], self.measurements[1])
        self.idle = ["idle", load_anims("idle", "ninja_animations/idle/", [12, 9, 7, 9])] 
        self.run = ["run", load_anims("run", "ninja_animations/run/", [5, 5, 5, 3])]
        self.fall = ["fall", load_anims("fall", "ninja_animations/fall/", [7])]
        self.jump = ["jump", load_anims("jump", "ninja_animations/jump/", [7])]
        self.anims = [self.idle, self.run, self.fall, self.jump]
        self.action = "fall"
        self.flip = False

frame = 0
anim_index = 0
max_frames = 0
max_anim_index = 0

(main loop now: )

for anim in ninja.anims:
        if ninja.action == anim[0]:
            if frame == 0:
                max_frames = anim[1][anim_index][1]
                max_anim_index = len(anim[1])
            else:
                if frame >= max_frames:
                    frame = 0
                    anim_index += 1
                    if anim_index >= max_anim_index:
                        anim_index = 0
                        frame = 0
                        max_frames = anim[1][anim_index][1]
            anim_image = pygame.image.load(anim[1][anim_index][0]).convert()
            anim_image.set_colorkey((255, 255, 255))
            if ninja.flip:
                anim_image = pygame.transform.flip(anim_image, True, False)
            screen.blit(anim_image, (ninja.rect.x - scroll[0], ninja.rect.y - scroll[1]))
            frame += 1