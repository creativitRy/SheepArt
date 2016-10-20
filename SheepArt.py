# SheepArt Generator
# by ctRy
# replaces blocks of wool with sheep

from collections import namedtuple
from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float

displayName = "SheepArt Generator"

Vector = namedtuple('Vector', 'x, y, z')

inputs = (
    ("SheepArt Generator by ctRy", "label"),
    ("replaces blocks of wool with sheep", "label"),
    
    ("Invulnerable:", True),
    ("Silent Sheep:", True),
    ("Fix lag by changing only outer blocks to sheep:", False),
)

def perform(level, box, options):
    inv = options["Invulnerable:"]
    fixLag = options["Fix lag by changing only outer blocks to sheep:"]

    temp = []

    for y in xrange(box.miny, box.maxy):
        for x in xrange(box.minx, box.maxx):
            for z in xrange(box.minz, box.maxz):
                if (level.blockAt(x, y, z) == 35):
                    if not fixLag or level.blockAt(x + 1, y, z) == 0 or level.blockAt(x, y + 1, z) == 0 or level.blockAt(x, y, z + 1) == 0 or level.blockAt(x - 1, y, z) == 0 or level.blockAt(x, y - 1, z) == 0 or level.blockAt(x, y, z - 1) == 0:
                        color = level.blockDataAt(x, y, z)

                        temp.append(Vector(x, y, z))

                        sheep = TAG_Compound()
                        sheep["Color"] = TAG_Byte(color)
                        sheep["PersistenceRequired"] = TAG_Byte(1)
                        sheep["OnGround"] = TAG_Byte(0)
                        sheep["Air"] = TAG_Short(300)
                        sheep["DeathTime"] = TAG_Short(0)
                        sheep["Fire"] = TAG_Short(-1)
                        sheep["Health"] = TAG_Float(8)
                        sheep["HurtTime"] = TAG_Short(0)
                        sheep["Age"] = TAG_Int(0)
                        sheep["FallDistance"] = TAG_Float(0)
                        sheep["Invulnerable"] = TAG_Byte(inv)
                        sheep["NoAI"] = TAG_Byte(1)
                        sheep["NoGravity"] = TAG_Byte(1)
                        sheep["Silent"] = TAG_Byte(options["Silent Sheep:"])
                        sheep["id"] = TAG_String("Sheep")
                        sheep["Motion"] = TAG_List([TAG_Double(0.0), TAG_Double(0.0), TAG_Double(0.0)])
                        sheep["Pos"] = TAG_List([TAG_Double(x + 0.5), TAG_Double(y), TAG_Double(z + 0.5)])
                        sheep["Rotation"] = TAG_List([TAG_Float(0), TAG_Float(0)])

                        chunk = level.getChunk(x / 16, z / 16)
                        chunk.Entities.append(sheep)
                        chunk.dirty = True

    while temp:
        cell = temp.pop()
        level.setBlockAt(cell.x, cell.y, cell.z, 0)
        level.setBlockDataAt(cell.x, cell.y, cell.z, 0)