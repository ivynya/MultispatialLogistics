import glob
import os

#writes list of stargates and info organized by parent system ID
#generateCSCode() depends on this functions output organization
def generateStargateList():
    #grab all files that contain stargate data
    files = glob.glob("sde\\fsd\\universe\\eve\\*\\*\\*\\solarsystem.staticdata")
    out = open("out.txt", "w")

    for file in files:
        data = open(file, 'r').read()
        #split data before and after systemID to get value
        sysID = data.split('solarSystemID:')[1].split('solarSystemNameID:')[0].strip()
        #split data before and after stargate info to get values, then split by line
        data = data.split('stargates:')[1].split('sunTypeID:')[0]
        data = data.split("\n")
        out.write((os.path.abspath(os.path.join(file, os.pardir))+"\n").split("\\")[-1])
        out.write(sysID)
        #write stripped lines to output
        for l in data:
            if(not("typeID" in l)):
                out.write(l.strip() + "\n")

#terrible way to get it into the SQL Database but here it is
def generateCSCode():
    data = open("out.txt", "r").read()
    lines = open("out.txt", "r").read().split("\n")
    cs = open("generatedCS.txt", "w")
    data = data.split("\n\n")
    for s in data:
        info = s.split("\n")
        ParentSystemId = (info[1])[0:8]
        ParentSystemName = info[0]
        StargateId = 0
        DestinationSystemId = 0
        DestinationStargateId = 0
        XPos = 0
        YPos = 0
        ZPos = 0
        for i in range(int((len(info)-1)/6)):
            StargateId = (info[(i*6)+2])[0:8]
            DestinationStargateId = (info[(i*6)+3])[13:22]
            #finds index of DestinationStargateId as a regular gate ID
            gatePos = lines.index(DestinationStargateId+":")
            #for 20 potential gates up, try and find ParentSystemId
            for z in range(0, 20):
                if (len(lines[gatePos-((z*6)+1)]) == 8):
                    DestinationSystemId = lines[gatePos-((z*6)+1)]
                    break
            XPos = (info[(i*6)+5])[2:]
            YPos = (info[(i*6)+6])[2:]
            ZPos = (info[(i*6)+7])[2:]
            cs = open("generatedCS.txt", "a")
            cs.write("new Stargate\n")
            cs.write("{\n")
            cs.write("    ParentSystemId = "+str(ParentSystemId)+",\n")
            cs.write("    ParentSystemName = \""+str(ParentSystemName)+"\",\n")
            cs.write("    StargateId = "+str(StargateId)+",\n")
            cs.write("    DestinationSystemId = "+str(DestinationSystemId)+",\n")
            cs.write("    DestinationStargateId = "+str(DestinationStargateId)+",\n")
            cs.write("    XPos = "+str(XPos[0:-2])+",\n")
            cs.write("    YPos = "+str(YPos[0:-2])+",\n")
            cs.write("    ZPos = "+str(ZPos[0:-2])+"\n")
            cs.write("},\n")

generateStargateList()
generateCSCode()
