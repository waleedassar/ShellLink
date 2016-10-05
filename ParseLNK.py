import os,sys,time
import struct,string
from datetime import datetime,timedelta


#-----------------------------------------------
BlockSignatureMap = ["EnvironmentVariableDataBlock","ConsoleDataBlock",\
                     "TrackerDataBlock","ConsoleFEDataBlock",\
                     "SpecialFolderDataBlock","DarwinDataBlock",\
                     "IconEnvironmentDataBlock","ShimDataBlock",\
                     "PropertyStoreDataBlock","UnknownDataBlock",\
                     "KnownFolderDataBlock", "VistaAndAboveIDListDataBlock"]

LinkFlagsMap = ["HasLinkTargetIDList","HasLinkInfo","HasName","HasRelativePath",\
                "HasWorkingDir","HasArguments","HasIconLocation","IsUnicode","ForceNoLinkInfo",\
                "HasExpString","RunInSeparateProcess","Unused1","HasDarwinID","RunAsUser","HasExpIcon",\
                "NoPidlAlias","Unused2","RunWithShimLayer","ForceNoLinkTrack","EnableTargetMetadata",\
                "DisableLinkPathTracking","DisableKnownFolderTracking","DisableKnownFolderAlias",\
                "AllowLinkToLink","UnaliasOnSave","PreferEnvironmentPath",\
                "KeepLocalIDListForUNCTarget","Unused3","Unused4","Unused5","Unused6","Unused7"]

FileAttributesMap = ["FILE_ATTRIBUTE_READONLY","FILE_ATTRIBUTE_HIDDEN","FILE_ATTRIBUTE_SYSTEM","Reserved1","FILE_ATTRIBUTE_DIRECTORY",\
                     "FILE_ATTRIBUTE_ARCHIVE","Reserved2","FILE_ATTRIBUTE_NORMAL","FILE_ATTRIBUTE_TEMPORARY",\
                     "FILE_ATTRIBUTE_SPARSE_FILE","FILE_ATTRIBUTE_REPARSE_POINT","FILE_ATTRIBUTE_COMPRESSED",\
                     "FILE_ATTRIBUTE_OFFLINE","FILE_ATTRIBUTE_NOT_CONTENT_INDEXED","FILE_ATTRIBUTE_ENCRYPTED"]
HotKeyFlags1Map=["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10",\
"F11","F12","F13","F14","F15","F16","F17","F18","F19","F20",\
"F21","F22","F23","2F4"]
HotKeyFlags1Map = ["HOTKEYF_SHIFT","HOTKEYF_CONTROL","HOTKEYF_ALT"]
DriveTypesMap = ["DRIVE_UNKNOWN","DRIVE_NO_ROOT_DIR","DRIVE_REMOVABLE","DRIVE_FIXED","DRIVE_REMOTE","DRIVE_CDROM","DRIVE_RAMDISK"]
FillAttributesMap = ["FOREGROUND_BLUE","FOREGROUND_GREEN",\
                     "FOREGROUND_RED","FOREGROUND_INTENSITY",\
                     "BACKGROUND_BLUE","BACKGROUND_GREEN",\
                     "BACKGROUND_RED","BACKGROUND_INTENSITY"]
#----------------------------------------------



def PrintFatalError(Err,ExitCode):
    print Err
    sys.exit(ExitCode)
    
def PrintInvalidHeaderError():
    PrintFatalError("Invalid Header Size\r\n",-4)

def PrintSmallError():
    PrintFatalError("Input file is too small\r\n",-3)

def GetDriveTypeString(InT):
    if InT > 6:
        return "DRIVE_UNKNOWN"
    return DriveTypesMap[InT]

def PrintHash(Hash):
    if Hash == "":
        return ""
    HashStr = ""
    HashLen = len(Hash)
    for i in range(0,HashLen):
        A = (hex(ord(Hash[i])).lower())[2:]
        if len(A) == 1:
            A = ("0" + A)
        HashStr += A
    return HashStr


def GetNetworkProviderString(ProvType):
    if ProvType == 0x001A0000:
	return "WNNC_NET_AVID"
    if ProvType == 0x001B0000:
        return "WNNC_NET_DOCUSPACE"
    if ProvType == 0x001C0000:
        return "WNNC_NET_MANGOSOFT"
    if ProvType == 0x001D0000:
        return "WNNC_NET_SERNET"
    if ProvType == 0X001E0000:
        return "WNNC_NET_RIVERFRONT1"
    if ProvType == 0x001F0000:
        return "WNNC_NET_RIVERFRONT2"
    if ProvType == 0x00200000:
        return "WNNC_NET_DECORB"
    if ProvType == 0x00210000:
        return "WNNC_NET_PROTSTOR"
    if ProvType == 0x00220000:
        return "WNNC_NET_FJ_REDIR"
    if ProvType == 0x00230000:
        return "WNNC_NET_DISTINCT"
    if ProvType == 0x00240000:
        return "WNNC_NET_TWINS"
    if ProvType == 0x00250000:
        return "WNNC_NET_RDR2SAMPLE"
    if ProvType == 0x00260000:
        return "WNNC_NET_CSC"
    if ProvType == 0x00270000:
        return "WNNC_NET_3IN1"
    if ProvType == 0x00290000:
        return "WNNC_NET_EXTENDNET"
    if ProvType == 0x002A0000:
        return "WNNC_NET_STAC"
    if ProvType == 0x002B0000:
        return "WNNC_NET_FOXBAT" 
    if ProvType == 0x002C0000:
        return "WNNC_NET_YAHOO" 
    if ProvType == 0x002D0000:
        return "WNNC_NET_EXIFS" 
    if ProvType == 0x002E0000:
        return "WNNC_NET_DAV"
    if ProvType == 0x002F0000:
        return "WNNC_NET_KNOWARE"
    if ProvType == 0x00300000:
        return "WNNC_NET_OBJECT_DIRE"
    if ProvType == 0x00310000:
        return "WNNC_NET_MASFAX"
    if ProvType == 0x00320000:
        return "WNNC_NET_HOB_NFS"
    if ProvType == 0x00330000:
        return "WNNC_NET_SHIVA"
    if ProvType == 0x00340000:
        return "WNNC_NET_IBMAL"
    if ProvType == 0x00350000:
        return "WNNC_NET_LOCK"
    if ProvType == 0x00360000:
        return "WNNC_NET_TERMSRV"
    if ProvType == 0x00370000:
        return "WNNC_NET_SRT"
    if ProvType == 0x00380000:
        return "WNNC_NET_QUINCY"
    if ProvType == 0x00390000:
        return "WNNC_NET_OPENAFS"
    if ProvType == 0X003A0000:
        return "WNNC_NET_AVID1"
    if ProvType == 0x003B0000:
        return "WNNC_NET_DFS"
    if ProvType == 0x003C0000:
        return "WNNC_NET_KWNP"
    if ProvType == 0x003D0000:
        return "WNNC_NET_ZENWORKS"
    if ProvType == 0x003E0000:
        return "WNNC_NET_DRIVEONWEB"
    if ProvType == 0x003F0000:
        return "WNNC_NET_VMWARE"
    if ProvType == 0x00400000:
        return "WNNC_NET_RSFX"
    if ProvType == 0x00410000:
        return "WNNC_NET_MFILES"
    if ProvType == 0x00420000:
        return "WNNC_NET_MS_NFS"
    if ProvType == 0x00430000:
        return "WNNC_NET_GOOGLE"
    return "UNKNOWN"
    
def GetItemIDTypeString(ItemType):
    if ItemType == 0x1F:
        return "VirtualObject"
    elif ItemType == 0x2F:
        return "Drive"
    elif ItemType == 0x31 or ItemType == 0x32:
        return "Folder/File"
    return "Unknown"

def GetNameFromSignatureId(SigId):
    SigId -= 0xA0000001;
    if SigId < 0xC:
        return BlockSignatureMap[SigId]
    return "Unsupported Block"

def IsKnownSignatureId(SigId):
    SigId -= 0xA0000001;
    if SigId < 0xC:
        if SigId == 0x9:
            return False
        else:
            return True
    return False
    
def PrintCLSID(fConX):
    listMapX = ["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f"]
    Length = len(fConX)
    #print hex(Length)
    if Length != 16:
        return ""
    CLSID = "{"
    XX =  ord(fConX[3])
    if XX < 0x10:
        CLSID += listMapX[XX]
    else:
        XXX = str(hex(XX))
        CLSID += XXX[2:4]
        
    YY =  ord(fConX[2])
    if YY < 0x10:
        CLSID += listMapX[YY]
    else:
        YYY = str(hex(YY))
        CLSID += YYY[2:4]
        
    ZZ =  ord(fConX[1])
    if ZZ < 0x10:
        CLSID += listMapX[ZZ]
    else:
        ZZZ = str(hex(ZZ))
        CLSID += ZZZ[2:4]
        
    AA =  ord(fConX[0])
    if AA < 0x10:
        CLSID += listMapX[AA]
    else:
        AAA = str(hex(AA))
        CLSID += AAA[2:4]
    
    CLSID += "-"
    
    BB =  ord(fConX[5])
    if BB < 0x10:
        CLSID += listMapX[BB]
    else:
        BBB = str(hex(BB))
        CLSID += BBB[2:4]
        
    CC =  ord(fConX[4])
    if CC < 0x10:
        CLSID += listMapX[CC]
    else:
        CCC = str(hex(CC))
        CLSID += CCC[2:4]
        
    CLSID += "-"
    
    DD =  ord(fConX[7])
    if DD < 0x10:
        CLSID += listMapX[DD]
    else:
        DDD = str(hex(DD))
        CLSID += DDD[2:4]
        
    EE =  ord(fConX[6])
    if EE < 0x10:
        CLSID += listMapX[EE]
    else:
        EEE = str(hex(EE))
        CLSID += EEE[2:4]
        
    CLSID += "-"
    
    FF =  ord(fConX[8])
    if FF < 0x10:
        CLSID += listMapX[FF]
    else:
        FFF = str(hex(FF))
        CLSID += FFF[2:4]
        
    GG =  ord(fConX[9])
    if GG < 0x10:
        CLSID += listMapX[GG]
    else:
        GGG = str(hex(GG))
        CLSID += GGG[2:4]
        
    CLSID += "-"
    HH = fConX[10:16]
    for ii in range(0,6):
        JJ = ord(HH[ii])
        if JJ < 0x10:
            CLSID += listMapX[JJ]
        else:
            JJJ = str(hex(JJ))
            CLSID+= JJJ[2:4]
    CLSID += "}"
    return CLSID


def ParseLinkInfoFlags(Flags):
    if Flags == 0:
        return "(No Flags)"
    Str = ""
    if Flags & 1:
        Str += ("VolumeIDAndLocalBasePath|")
    if Flags & 2:
        Str += ("CommonNetworkRelativeLinkAndPathSuffix|")
    if Flags & 0xFFFFFFFC:
        Str += ("Unknown|")
    return Str.rstrip("|")

def PrintDriveSerialNumber(fConXX):
    listMapX = ["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f"]
    fConX = struct.pack("L",fConXX)
    Length = len(fConX)
    if Length != 4:
        return ""
    SN = ""
    XX =  ord(fConX[3])
    if XX < 0x10:
        SN += listMapX[XX]
    else:
        XXX = str(hex(XX))
        SN += XXX[2:4]
        
    YY =  ord(fConX[2])
    if YY < 0x10:
        SN += listMapX[YY]
    else:
        YYY = str(hex(YY))
        SN += YYY[2:4]

    SN += "-"
    
    ZZ =  ord(fConX[1])
    if ZZ < 0x10:
        SN += listMapX[ZZ]
    else:
        ZZZ = str(hex(ZZ))
        SN += ZZZ[2:4]
        
    AA =  ord(fConX[0])
    if AA < 0x10:
        SN += listMapX[AA]
    else:
        AAA = str(hex(AA))
        SN += AAA[2:4]
    SN = SN.upper()
    return SN



def GetMyPrintables():
    Printables = string.printable
    NewPrintables = ""
    lenPrintables = len(Printables)
    for i in range(0,lenPrintables):
        if ord(Printables[i]) >= 9 and ord(Printables[i]) <= 13:
            pass
        else:
            NewPrintables += Printables[i]
    return NewPrintables

def GetCString_U(Data):
    Str = ""
    if Data == "":
        return ""
    DataLen = len(Data)
    MyPrint = string.printable
    for i in range(0,DataLen,2):
        XXX = Data[i:i+2]
        if len(XXX) == 2 and XXX[0]=="\x00" and XXX[1]=="\x00":
            #print Str.decode("utf-16").encode("utf-8")
            return Str.decode("utf-16").encode("utf-8")
        else:
            Str += XXX
    return ""

def ExtractAllStrings_U(Data):
    if Data == "":
        return []
    Final = []
    DataLen = len(Data)
    i = 0
    EndFound = False
    while EndFound == False and i < DataLen:
        XX = Data[i:]
        UStr = GetCString_U(XX)
        if UStr == "":
            EndFound = True
            break
        else:
            Final.append(UStr)
        i += ((len(UStr)*2)+2)
    return Final
        

def GetCString_A(Data):
    Str = ""
    if Data == "":
        return ""
    DataLen = len(Data)
    MyPrint = string.printable
    for i in range(0,DataLen):
        if ord(Data[i])==0:
            return Str
        else:
            X = Data[i]
            if MyPrint.find(X) != -1:
                Str += X
            else:
                return ""
    return "" 

def ExtractAllStrings_A(Data):
    if Data == "":
        return []
    Final = []
    DataLen = len(Data)
    i = 0
    EndFound = False
    while EndFound == False and i < DataLen:
        XX = Data[i:]
        AStr = GetCString_A(XX)
        if AStr == "":
            EndFound = True
            break
        else:
            Final.append(UStr)
        i += (len(UStr)+1)
    return Final



def ParseCommonPathSuffix(LinkInfo,LinkInfoSize,CommonPathSuffixOffset,CommonPathSuffixOffsetUnicode):
    if LinkInfo == "" or len(LinkInfo) != LinkInfoSize or CommonPathSuffixOffset >= LinkInfoSize or \
       CommonPathSuffixOffsetUnicode >= LinkInfoSize:
        return {}

    dictX = {}
    dictX["Type"] = "CommonPathSuffix"
    
    _Unicode = False
    if CommonPathSuffixOffset == 0 and CommonPathSuffixOffsetUnicode != 0:
        _Unicode = True

    Offset = 0
    if _Unicode == True:
        Offset = CommonPathSuffixOffsetUnicode
    else:
        Offset = CommonPathSuffixOffset
        
    if Offset <= 0x10:
        return {}

    dictX["CommonPathSuffixA"] = ""
    dictX["CommonPathSuffixU"] = ""
    CommonPathSuffix = ""
    if _Unicode == True:
        Offset = CommonPathSuffixOffsetUnicode
        #print len(LinkInfo[Offset:])
        CommonPathSuffix = GetCString_U(LinkInfo[Offset:])
        dictX["CommonPathSuffixU"] = CommonPathSuffix
    else:
        Offset = CommonPathSuffixOffset
        #print len(LinkInfo[Offset:])
        CommonPathSuffix = GetCString_A(LinkInfo[Offset:])
        dictX["CommonPathSuffixA"] = CommonPathSuffix
    #print "CommonPathSuffix: " + CommonPathSuffix
    return dictX



def ParseLocalBasePath(LinkInfo,LinkInfoSize,LocalBasePathOffset,LocalBasePathOffsetUnicode):
    if LinkInfo == "" or len(LinkInfo) != LinkInfoSize or LocalBasePathOffset >= LinkInfoSize or \
       LocalBasePathOffsetUnicode >= LinkInfoSize:
        return {}
    
    dictX = {}
    dictX["Type"] = "LocalBasePath"
    
    _Unicode = False
    if LocalBasePathOffset == 0 and LocalBasePathOffsetUnicode != 0:
        _Unicode = True

    Offset = 0
    if _Unicode == True:
        Offset = LocalBasePathOffsetUnicode
    else:
        Offset = LocalBasePathOffset
        
    if Offset <= 0x10:
        return {}
    dictX["LocalBasePathA"] = ""
    dictX["LocalBasePathU"] = ""
    BasePath = ""
    if _Unicode == True:
        Offset = LocalBasePathOffsetUnicode
        BasePath = GetCString_U(LinkInfo[Offset:])
        dictX["LocalBasePathU"] = BasePath
    else:
        Offset = LocalBasePathOffset
        BasePath = GetCString_A(LinkInfo[Offset:])
        dictX["LocalBasePathA"] = BasePath
    #print "LocalBasePath: " + BasePath
    return dictX
    
def ParseVolumeID(LinkInfo,LinkInfoSize,VolumeIDOffset):
    if LinkInfo == "" or len(LinkInfo) != LinkInfoSize or VolumeIDOffset >= LinkInfoSize:
        return {}
    if VolumeIDOffset <= 0x10:
        return {}
    if VolumeIDOffset + 4 >= LinkInfoSize:
        return {}
    VolumeIDSize = struct.unpack("L",LinkInfo[VolumeIDOffset:VolumeIDOffset+4])[0]
    
    if VolumeIDOffset + VolumeIDSize > LinkInfoSize:
        return {}

    DictX = {}
    DictX["Type"] = "Volume"
    
    VolumeID = LinkInfo[VolumeIDOffset:VolumeIDOffset+VolumeIDSize]

    
    DriveType_ = struct.unpack("L",VolumeID[4:8])[0]
    #print "DriveType: " + hex(DriveType_) + " (" + GetDriveTypeString(DriveType_) +")"
    DictX["DriveType"] = DriveType_

    DriveSerialNumber = struct.unpack("L",VolumeID[8:0xC])[0]
    #print "Drive SerialNo: " + hex(DriveSerialNumber) + " (" + PrintDriveSerialNumber(DriveSerialNumber) + ")"
    DictX["DriveSerialNumber"] = DriveSerialNumber
    
    VolumeLabelOffset = struct.unpack("L",VolumeID[0xC:0x10])[0]
    if VolumeLabelOffset >= VolumeIDSize:
        return {}
    #print hex(VolumeLabelOffset)
    
    VolumeLabelOffsetUnicode = False
    VolumeLabelOffsetUnicode_ = 0
    if VolumeLabelOffset == 0x14:
        VolumeLabelOffsetUnicode = True
        VolumeLabelOffsetUnicode_ = struct.unpack("L",VolumeID[0x10:0x14])[0]
        if VolumeLabelOffsetUnicode_ > VolumeIDSize:
            return {}
    #print hex(VolumeLabelOffsetUnicode_)
    DictX["VolumeA"] = ""
    DictX["VolumeU"] = ""
    VolumeString = ""
    if VolumeLabelOffsetUnicode == True:
        VolumeString =  GetCString_U(VolumeID[VolumeLabelOffsetUnicode_:])
        DictX["VolumeU"] = VolumeString
    else:
        VolumeString = GetCString_A(VolumeID[VolumeLabelOffset:])
        DictX["VolumeA"] = VolumeString
    #print "Drive Name: " + VolumeString
    return DictX
    

#This function has not been tested against real .LNK files
def ParseCommonNetworkRelativeLink(LinkInfo,LinkInfoSize,CommonNetworkRelativeLinkOffset):
    if LinkInfo == "" or len(LinkInfo) != LinkInfoSize or CommonNetworkRelativeLinkOffset >= LinkInfoSize:
        return {}
    if CommonNetworkRelativeLinkOffset <= 0x10:
        return {}
    if CommonNetworkRelativeLinkOffset + 4 >= LinkInfoSize:
        return {}

    dictX["Type"] = "CommonNetworkRelativeLink"
    
    CommonNetworkRelativeLinkSize = struct.unpack("L",LinkInfo[CommonNetworkRelativeLinkOffset:CommonNetworkRelativeLinkOffset+4])[0]
    
    if CommonNetworkRelativeLinkOffset + CommonNetworkRelativeLinkSize > LinkInfoSize:
        return {}

    Common = LinkInfo[CommonNetworkRelativeLinkOffset:CommonNetworkRelativeLinkOffset+CommonNetworkRelativeLinkSize]
    
    CommonNetworkRelativeLinkFlags = struct.unpack("L",Common[4:8])[0]
    #print "CommonNetworkRelativeLinkFlags: " + hex(CommonNetworkRelativeLinkFlags)


    NetNameOffset = struct.unpack("L",Common[8:0xC])[0]
    #print "NetNameOffset: " + hex(DriveSerialNumber)

    
    DeviceNameOffset = struct.unpack("L",Common[0xC:0x10])[0]
    if DeviceNameOffset >= CommonNetworkRelativeLinkSize:
        return ""
    #print "DeviceNameOffset: " + hex(VolumeLabelOffset)

    NetworkProviderType = struct.unpack("L",Common[0x10:0x14])[0]
    #print "NetworkProviderType: " + hex(NetworkProviderType)
    dictX["NetworkProviderType"] = NetworkProviderType
    
    NetNameOffsetUnicodeExists = False
    NetNameOffsetUnicode_ = 0
    if NetNameOffset > 0x14:
        NetNameOffsetUnicodeExists = True
        NetNameOffsetUnicode_ = struct.unpack("L",Common[0x14:0x18])[0]
        if NetNameOffsetUnicode_ > CommonNetworkRelativeLinkSize:
            return {}

    DeviceNameOffsetUnicodeExists = False
    DeviceNameOffsetUnicode_ = 0
    if NetNameOffset > 0x14:
        DeviceNameOffsetUnicodeExists = True
        DeviceNameOffsetUnicode_ = struct.unpack("L",Common[0x18:0x1C])[0]
        if DeviceNameOffsetUnicode_ > CommonNetworkRelativeLinkSize:
            return {}
    

    NetName_A = ""
    NetName_U = ""
    
    NetName_A =  GetCString_A(Common[NetNameOffset:])
    #print NetName_A
    dictX["NetNameA"] = NetName_A
    

    if NetNameOffsetUnicodeExists == True:
        NetName_U =  GetCString_U(Common[NetNameOffsetUnicode_:])
        #print NetName_U
    dictX["NetNameU"] = NetName_U

    DeviceName_A = ""
    DeviceName_U = ""
    
    DeviceName_A =  GetCString_A(Common[DeviceNameOffset:])
    #print DeviceName_A
    dictX["DeviceNameA"] = DeviceName_A

    if DeviceNameOffsetUnicodeExists == True:
        DeviceName_U =  GetCString_U(Common[DeviceNameOffsetUnicode_:])
        #print DeviceName_U
    dictX["DeviceNameU"] = DeviceName_U
    return dictX

    
def ParseLinkInfo(LinkInfo,LinkInfoSize,LinkInfoHeader,LinkInfoHeaderSize):
    if LinkInfo == "" or LinkInfoHeader == "" or len(LinkInfo) != LinkInfoSize or len(LinkInfoHeader) != LinkInfoHeaderSize:
        return []
    if LinkInfoHeaderSize >= LinkInfoSize:
        return []
    
    if LinkInfoHeaderSize < 0x1C:
        return []
    
    gOptional = False
    if LinkInfoHeaderSize > 0x1C:
        gOptional = True

    #print "LinkInfoSize: " + hex(LinkInfoSize)
    #print "LinkInfoHeaderSize: " + hex(LinkInfoHeaderSize)
    LinkInfoFlags = struct.unpack("L",LinkInfoHeader[0x8:0xC])[0]
    print "LinkInfoFlags: " + hex(LinkInfoFlags) + " (" + ParseLinkInfoFlags(LinkInfoFlags) + ")"
    VolumeIDOffset = struct.unpack("L",LinkInfoHeader[0xC:0x10])[0]
    print "VolumeIDOffset: " + hex(VolumeIDOffset)
    LocalBasePathOffset = struct.unpack("L",LinkInfoHeader[0x10:0x14])[0]
    print "LocalBasePathOffset: " + hex(LocalBasePathOffset)
    CommonNetworkRelativeLinkOffset = struct.unpack("L",LinkInfoHeader[0x14:0x18])[0]
    print "CommonNetworkRelativeLinkOffset: " + hex(CommonNetworkRelativeLinkOffset)
    CommonPathSuffixOffset = struct.unpack("L",LinkInfoHeader[0x18:0x1C])[0]
    print "CommonPathSuffixOffset: " + hex(CommonPathSuffixOffset)

    LocalBasePathOffsetUnicode = False
    CommonPathSuffixOffsetUnicode = False
    LocalBasePathOffsetUnicode_ = 0
    CommonPathSuffixOffsetUnicode_ = 0
    if LinkInfoHeaderSize >= 0x20:
        LocalBasePathOffsetUnicode_ = struct.unpack("L",LinkInfoHeader[0x1C:0x20])[0]
        if LocalBasePathOffsetUnicode_ != 0:
            LocalBasePathOffsetUnicode = True
    if LinkInfoHeaderSize >= 0x24:
        CommonPathSuffixOffsetUnicode_ = struct.unpack("L",LinkInfoHeader[0x20:0x24])[0]
        if CommonPathSuffixOffsetUnicode_ != 0:
            CommonPathSuffixOffsetUnicode = True
    print "LocalBasePathOffsetUnicode: " + hex(LocalBasePathOffsetUnicode_)
    print "CommonPathSuffixOffsetUnicode: " + hex(CommonPathSuffixOffsetUnicode_)

    #Check offsets validity
    if VolumeIDOffset >= LinkInfoSize or \
       LocalBasePathOffset >= LinkInfoSize or \
       CommonNetworkRelativeLinkOffset >= LinkInfoSize or \
       CommonPathSuffixOffset >= LinkInfoSize or \
       LocalBasePathOffsetUnicode_ >= LinkInfoSize or \
       CommonPathSuffixOffsetUnicode_ >= LinkInfoSize:
        return []
    dList = []
    ret1 = ParseVolumeID(LinkInfo,LinkInfoSize,VolumeIDOffset)
    ret2 = ParseLocalBasePath(LinkInfo,LinkInfoSize,LocalBasePathOffset,LocalBasePathOffsetUnicode_)
    ret3 = ParseCommonNetworkRelativeLink(LinkInfo,LinkInfoSize,CommonNetworkRelativeLinkOffset)
    ret4 = ParseCommonPathSuffix(LinkInfo,LinkInfoSize,CommonPathSuffixOffset,CommonPathSuffixOffsetUnicode_)
    dList.append(ret1)
    dList.append(ret2)
    dList.append(ret3)
    dList.append(ret4)
    return dList
    
       

def ParseFolderOrFileItemID(ItemID,ItemIDSize):
    if ItemID == "" or ItemIDSize != len(ItemID):
        return ""
    sFileFolder = ""
    if ItemIDSize >= 1:
        ItemType = ord(ItemID[0])
        if ItemType != 0x31 and ItemType != 0x32:
            return sFileFolder
    #Only tested on Windows 10
    if ItemIDSize > 0xC:
        FolderOrFile = ItemID[0xC:]
        sFileFolder = GetCString_A(FolderOrFile)    
    return sFileFolder
    
def ParseVolumeItemID(ItemID,ItemIDSize):
    if ItemID == "" or ItemIDSize != len(ItemID):
        return ""
    sVolumeName = ""
    if ItemIDSize >= 1:
        ItemType = ord(ItemID[0])
        if ItemType != 0x2F:
            return sVolumeName
    if ItemIDSize >= 2:
        VolumeName = ItemID[1:]
        sVolumeName =  GetCString_A(VolumeName)    
    return sVolumeName

def ParseVirtualItemID(ItemID,ItemIDSize):
    if ItemID == "" or ItemIDSize != len(ItemID):
        return ""
    clsid = ""
    if ItemIDSize >= 1:
        ItemType = ord(ItemID[0])
        if ItemType != 0x1F:
            return clsid
    if ItemIDSize >= 2:
        SortOrder = ord(ItemID[1])
    if ItemIDSize >= 18:
        FolderId = ItemID[2:18]
        clsid = PrintCLSID(FolderId)
    return clsid
        
def ParseItemId(ItemID,ItemIDSize):
    if ItemID == "" or ItemIDSize != len(ItemID):
        return ""
    ItemType = 0
    if ItemIDSize >= 1:
        ItemType = ord(ItemID[0])
    FullPath = ""

    IDTypeStr = GetItemIDTypeString(ItemType)
    #print "ItemType: " + hex(ItemType) + " " + IDTypeStr
    
    #Virtual Object e.g. My Computer
    if ItemType == 0x1F:
        FullPath = ( IDTypeStr + "!!!" + ParseVirtualItemID(ItemID,ItemIDSize))
    #Volume/Drive
    elif ItemType == 0x2F:
        FullPath = (IDTypeStr + "!!!" + ParseVolumeItemID(ItemID,ItemIDSize))
    #Folder Or File
    elif ItemType == 0x31 or ItemType == 0x32:
        FullPath = (IDTypeStr + "!!!" + ParseFolderOrFileItemID(ItemID,ItemIDSize))
    else:
        FullPath = (IDTypeStr + "!!!" + ParseFolderOrFileItemID(ItemID,ItemIDSize))
    return FullPath

        
#return Number of read ItemIDs
def ParseIDList(IDList,IDListSize):
    if IDList == "" or IDListSize != len(IDList) or IDListSize < 2:
        return []
    EndFound = False
    i = 0
    FullPath = []
    PathPart = ""
    while EndFound == False:
        ItemIDSize = struct.unpack("H",IDList[i:i+2])[0]
        #print "ItemID Size: " + hex(ItemIDSize)
        if ItemIDSize == 0:
            EndFound = True
        else:
            if i + ItemIDSize > IDListSize:
                return []
            ItemID = IDList[i+2:i+ItemIDSize]
            ItemIDOffset = i
            print "Now parsing ItemID at offset: " + hex(ItemIDOffset)
            i += ItemIDSize
            PathPart = ParseItemId(ItemID,ItemIDSize-2)
            if PathPart != "":
                FullPath.append(str(ItemIDOffset) + "!!!"+ str(ItemIDSize) + "!!!" + PathPart) #Offset!!!Size!!!Type!!!Value
    return FullPath

def ParseSerializedPropertyValueString(SerializedPropertyValue,SerializedPropertyValueLen):
    if SerializedPropertyValue == "" or len(SerializedPropertyValue)!=SerializedPropertyValueLen:
        return ""
    if SerializedPropertyValueLen < 4:
        return ""
    ValueSize = struct.unpack("L",SerializedPropertyValue[0:4])[0]
    print "ValueSize: " + hex(ValueSize)
    i = 4
    if i > SerializedPropertyValueLen:
        return ""
    NameSize = struct.unpack("L",SerializedPropertyValue[i:i+4])[0]
    print "NameSize: " + hex(NameSize)
    i += 4
    if (ValueSize + NameSize + 9) > SerializedPropertyValueLen:
        return ""

    Reserved = ord(SerializedPropertyValue[i:i+1])
    if Reserved != 0:
        print "Invalid Reserved value\r\n"
    i += 1
    
    Name = SerializedPropertyValue[i:i+NameSize]
    i += NameSize
    print GetCString_U(Name)

    Value = SerializedPropertyValue[i:i+ValueSize]
    i += ValueSize
    #Handle MS_OLEPS
    return ""

    
def ParseSerializedPropertyValueInteger(SerializedPropertyValue,SerializedPropertyValueLen):
    if SerializedPropertyValue == "" or len(SerializedPropertyValue)!=SerializedPropertyValueLen:
        return ""
    if SerializedPropertyValueLen < 4:
        return ""
    ValueSize = struct.unpack("L",SerializedPropertyValue[0:4])[0]
    print "ValueSize: " + hex(ValueSize)
    i = 4
    if i > SerializedPropertyValueLen:
        return ""
    PropertyId = struct.unpack("L",SerializedPropertyValue[i:i+4])[0]
    print "PropertyId: " + hex(PropertyId)
    i += 4

    
    if (ValueSize + 9) > SerializedPropertyValueLen:
        return ""
    Reserved = ord(SerializedPropertyValue[i:i+1])
    if Reserved != 0:
        print "Invalid Reserved value\r\n"
    i += 1

    Value = SerializedPropertyValue[i:i+ValueSize]
    i += ValueSize
    #Handle MS_OLEPS
    return ""

    
def ParseSerializedPropertyValue(SerializedPropertyValue,Guid):
    if SerializedPropertyValue == "" or len(Guid) != 38:
        return ""
    xGuid = Guid.lower()
    SerializedPropertyValueLen = len(SerializedPropertyValue)
    if xGuid == "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}":
        return ParseSerializedPropertyValueString(SerializedPropertyValue,SerializedPropertyValueLen)
    else:
        return ParseSerializedPropertyValueInteger(SerializedPropertyValue,SerializedPropertyValueLen)
    return ""
        
        
    
def ParsePropertyStore(PropertyStore,PropertyStoreSize):
    if PropertyStore == "" or len(PropertyStore) != PropertyStoreSize:
        return []
    if PropertyStoreSize < 4:
        return []

    Prop = ""
    FinalProps = []
    
    
    TerminalFound = False

    i = 0
    while TerminalFound == False and i < PropertyStoreSize:
        Prop = ""
        if i + 4 <= PropertyStoreSize:
            StorageSize = struct.unpack("L",PropertyStore[i:i+4])[0]
            i += 4
            print "StoreSize: " + hex(StorageSize)
            if StorageSize == 0:
                print "Terminal of Serialized Properties found\r\n"
                TerminalFound = True
                break
        if i + 0x14 <= PropertyStoreSize:
            Version = struct.unpack("L",PropertyStore[i:i+4])[0]
            i += 4
            print "Version: " + hex(Version)
            if Version != 0x53505331:
                print "Invalid version\r\n"
            FormatID = PropertyStore[i:i+16]
            i += 16
            Clsid = PrintCLSID(FormatID).rstrip().lstrip()
            Prop += Clsid #38 chars
            print "Format ID: " + Clsid

            Left = StorageSize - 0x18
            SerializedPropertyValue = ""
            if Left > 0:
               SerializedPropertyValue = PropertyStore[i:i+Left]
            else:
                print "Empty serialized property value\r\n"
            i += Left

            
            Prop += SerializedPropertyValue
            #print Prop
            FinalProps.append(Prop)
            Prop = ""
                      
    if TerminalFound == False:
        print "Terminal of Serialized Properties Not Found\r\n"
    return FinalProps
    


def ParsePropertyStoreDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    print "DataBlockSize: " + hex(DataBlockSize)
    if DataBlockSize < 0x00000C:
        return ""
    i = 8
    
    PropertyStore = DataBlock[i:]
    print "PropertyStore: " + PrintHash(PropertyStore)
    FormatIDsAndSerializedPropertyValues= ParsePropertyStore(PropertyStore,DataBlockSize-8)
    for x in FormatIDsAndSerializedPropertyValues:
        Clsid = x[0:38]
        SerializedPropertyValue = x[38:]
        ParseSerializedPropertyValue(SerializedPropertyValue,Clsid)

        


    
def ParseKnownFolderDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize != 0x1C:
        return ""
    i = 8
    FStr = ""
    KnownFolderID = DataBlock[i:i+16]
    i += 16
    Str = ( "FolderId: " + PrintCLSID(KnownFolderID) )
    print Str
    FStr += (Str + "\r\n")

    Offset = hex(struct.unpack("L",DataBlock[i:i+4])[0])
    i += 4
    #This should be matched with LinkTargetIDList
    Str = ( "Offset: " + Offset )
    print Str
    FStr += (Str + "\r\n")
    return FStr

    


        
        
    
def ParseShimDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize < 0x0000088:
        return ""
    i = 8
    
    LayerName = DataBlock[i:]
    FStr = ( "LayerName: " + GetCString_U(LayerName+"\x00\x00") )
    return FStr

    
def ParseIconEnvironmentDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize != 0x00000314:
        return ""
    i = 8
    FStr = ""
    TargetAnsi = DataBlock[i:i+260]
    i += 260
    Str = ( "TargetAnsi: " + GetCString_A(TargetAnsi) )
    print Str
    FStr += (Str + "\r\n")
    
    TargetUnicode = DataBlock[i:i+520]
    i += 520
    Str = ( "TargetUnicode: " + GetCString_U(TargetUnicode) )
    print Str
    FStr += (Str + "\r\n")
    return FStr


    

def ParseDarwinDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize != 0x00000314:
        return ""
    i = 8
    FStr = ""
    
    DarwinDataAnsi = DataBlock[i:i+260]
    i += 260
    Str = ( "DarwinDataAnsi: " + GetCString_A(DarwinDataAnsi) )
    print Str
    FStr += (Str + "\r\n")
    
    DarwinDataUnicode = DataBlock[i:i+520]
    i += 520
    Str = ( "DarwinDataUnicode: " + GetCString_U(DarwinDataUnicode) )
    print Str
    FStr += (Str + "\r\n")
    return FStr

    
def ParseSpecialFolderDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize != 0x10:
        return ""
    i = 8
    FStr = ""
    
    FolderId = hex(struct.unpack("L",DataBlock[i:i+4])[0])
    i += 4
    Str = ( "FolderId: " + FolderId )
    print Str
    FStr += (Str + "\r\n")

    LinkTargetIDListOffset = hex(struct.unpack("L",DataBlock[i:i+4])[0])
    i += 4
    #This should be matched with LinkTargetIDList
    Str = ( "LinkTargetIDListOffset: " + LinkTargetIDListOffset )
    print Str
    FStr += (Str + "\r\n")
    return FStr




def ParseConsoleFEDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize != 0x000000C:
        return ""
    i = 8
    
    CodePage = hex(struct.unpack("L",DataBlock[i:i+4])[0])
    i += 4
    FStr = ( "CodePage: " + (CodePage) )
    print FStr
    return (FStr + "\r\n")

def ParseTrackerDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize != 0x00000060:
        return ""
    i = 8
    
    Length = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    if Length != 0x58:
        return ""
    FStr = ""
    
    Version = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    Str =  ("Version: " + hex(Version))
    print Str
    FStr += (Str+"\r\n")
    
    MachineID = DataBlock[i:i+16]
    i += 16
    Str = ( "MachineID: " + GetCString_A(MachineID) )
    print Str
    FStr += (Str+"\r\n")
    
    Droid = DataBlock[i:i+32]
    i += 32
    Str = ( "Droid: " + PrintHash(Droid) )
    print Str
    FStr += (Str+"\r\n")

    DroidBirth = DataBlock[i:i+32]
    i += 32
    Str = ( "DroidBirth: " + PrintHash(DroidBirth) )
    print Str
    FStr += (Str+"\r\n")

    return FStr


def ParseEnvironmentVariableDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize != 0x00000314:
        return ""
    A = DataBlock[8:0x10C]
    U = DataBlock[0x10C:]
    A_Str = GetCString_A(A)
    U_Str = GetCString_U(U)
    
    FStr = "EnvironmentVariable_ANSI: " + A_Str + "\r\nEnvironmentVariable_ANSI: " + U_Str + "\r\n"
    return FStr




def GetFontFamilyString(FamX):
    if FamX == 0:
        return "FF_DONTCARE"
    elif FamX == 0x10:
        return "FF_ROMAN"
    elif FamX == 0x20:
        return "FF_SWISS"
    elif FamX == 0x30:
        return "FF_MODERN"
    elif FamX == 0x40:
        return "FF_SCRIPT"
    elif FamX == 0x50:
        return "FF_DECORATIVE"
    else:
        return "Unknown"
    
def GetFillAttributesString(AttX):
    StrX = ""
    if AttX == 0:
        return "(Empty)"
    for i in range(0,8):
        XX = 1 << i
        if AttX & XX:
            StrX += ( FillAttributesMap[i] + "|")
    if AttX & 0xFFFFFF00:
        StrX += "Unknown"
    return StrX.rstrip("|")
        
def ParseConsoleDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize != 0x00000CC:
        return ""
    i = 8
    FStr = ""
    FillAttributes = struct.unpack("H",DataBlock[i:i+2])[0]
    i += 2
    Str =  ("FillAttributes: " + hex(FillAttributes) + " (" + GetFillAttributesString(FillAttributes) + ")")
    print Str
    FStr += ( Str + "\r\n")
    
    PopupFillAttributes = struct.unpack("H",DataBlock[i:i+2])[0]
    i += 2
    Str = ("PopupFillAttributes: " + hex(PopupFillAttributes) + " (" + GetFillAttributesString(PopupFillAttributes) + ")")
    print Str
    FStr += (Str + "\r\n")
    
    ScreenBufferSizeX = struct.unpack("H",DataBlock[i:i+2])[0]
    i += 2
    Str = ("ScreenBufferSizeX: " + hex(ScreenBufferSizeX))
    print Str
    FStr += (Str + "\r\n")
    
    ScreenBufferSizeY = struct.unpack("H",DataBlock[i:i+2])[0]
    i += 2
    Str = ("ScreenBufferSizeY: " + hex(ScreenBufferSizeY))
    print Str
    FStr += (Str + "\r\n")
    
    WindowSizeX = struct.unpack("H",DataBlock[i:i+2])[0]
    i += 2
    Str = ("WindowSizeX: " + hex(WindowSizeX))
    print Str
    FStr += (Str + "\r\n")
    
    WindowSizeY = struct.unpack("H",DataBlock[i:i+2])[0]
    i += 2
    Str = ( "WindowSizeY: " + hex(WindowSizeY) )
    print Str
    FStr += (Str + "\r\n")
    
    WindowOriginX = struct.unpack("H",DataBlock[i:i+2])[0]
    i += 2
    Str = ("WindowOriginX: " + hex(WindowOriginX))
    print Str
    FStr += (Str + "\r\n")
    
    WindowOriginY = struct.unpack("H",DataBlock[i:i+2])[0]
    i += 2
    Str = ("WindowOriginY: " + hex(WindowOriginY))
    print Str
    FStr += (Str + "\r\n")
    
    Unused1 = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    Str = ("Unused1: " + hex(Unused1))
    print Str
    FStr += (Str + "\r\n")
    
    
    Unused2 = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    Str = ( "Unused2: " + hex(Unused2) )
    print Str
    FStr += (Str + "\r\n")
    
    
    FontSize = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    Str = ( "FontSize: " + hex(FontSize) )
    print Str
    FStr += (Str + "\r\n")
    
    FontFamily = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    Str = ( "FontFamily: " + hex(FontFamily) + " (" + GetFontFamilyString(FontFamily) + ")" )
    print Str
    FStr += (Str + "\r\n")
    
    
    FontWeight = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    sFontWeight = ""
    if FontWeight <= 700:
        sFontWeight = "Bold font"
    else:
        sFontWeight = "Regular-weight font"
    Str = ( "FontWeight: " + hex(FontWeight) + " (" + sFontWeight + ")" )
    print Str
    FStr += (Str + "\r\n")
    
    
    FaceName = ExtractAllStrings_U(DataBlock[i:i+64]+"\x00\x00")
    i += 64
    Str = ( "FaceName: " + str(FaceName) )
    print Str
    FStr += (Str + "\r\n")
    
    CursorSize = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    sCursorSize = ""
    if CursorSize <= 25:
        sCursorSize = "Small cursor"
    elif CursorSize >= 26 and CursorSize <= 50:
        sCursorSize = "Medium cursor"
    elif CursorSize >= 51 and CursorSize <= 100:
        sCursorSize = "Large cursor"
    else:
        sCursorSize = "Unknown size"
    Str = ( "CursorSize: " + hex(CursorSize) + " (" + sCursorSize + ")" )
    print Str
    FStr += (Str + "\r\n")
    
    FullScreen = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    sFullScreen = "Off"
    if FullScreen != 0:
        sFullScreen = "On"
    Str = ( "FullScreen: " + hex(FullScreen) + " (" + sFullScreen + ")" )
    print Str
    FStr += (Str + "\r\n")
    
    QuickEdit = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    sQuickEdit = "Off"
    if QuickEdit != 0:
        sQuickEdit = "On"
    Str = ( "QuickEdit: " + hex(QuickEdit) + " (" + sQuickEdit + ")")
    print Str
    FStr += (Str + "\r\n")
    
    
    InsertMode = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    sInsertMode = "Off"
    if InsertMode != 0:
        sInsertMode = "On"
    Str = ( "InsertMode: " + hex(InsertMode) + " (" + sInsertMode + ")" )
    print Str
    FStr += (Str + "\r\n")
    
    AutoPosition = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    sAutoPosition = "Off"
    if AutoPosition != 0:
        sAutoPosition = "On"
    Str = ( "AutoPosition: " + hex(AutoPosition) + " (" + sAutoPosition + ")" )
    print Str
    FStr += (Str + "\r\n")
    
    HistoryBufferSize = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    Str = ( "HistoryBufferSize: " + hex(HistoryBufferSize) )
    print Str
    FStr += (Str + "\r\n")
    
    NumberOfHistoryBuffers = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    Str = ( "NumberOfHistoryBuffers: " + hex(NumberOfHistoryBuffers) )
    print Str
    FStr += (Str + "\r\n")
    
    HistoryNoDup = struct.unpack("L",DataBlock[i:i+4])[0]
    i += 4
    sHistoryNoDup = "Duplicates not allowed"
    if HistoryNoDup != 0:
        sHistoryNoDup = "Duplicates allowed"
    Str = ( "HistoryNoDup: " + hex(HistoryNoDup) + " (" + sHistoryNoDup + ")" )
    print Str
    FStr += (Str + "\r\n")
    
    ColorTable = DataBlock[i:i+64]
    i += 64
    #print ParseColorTable(ColorTable)
    Str = ( "Color Table: " + PrintHash(ColorTable) )
    print Str
    FStr += (Str + "\r\n")

    return FStr
    
def ParseVistaAndAboveIDListDataBlock(DataBlock,DataBlockSize):
    if DataBlock == "" or len(DataBlock) != DataBlockSize:
        return ""
    if DataBlockSize < 0xA:
        return ""
    i = 8
    FStr = ""
    IDListSize = DataBlockSize - i
    IDList = DataBlock[i:]
    #print "IDList: " + PrintHash(IDList)
    #This should be handled the same way as LinkTargetIDList
    IDs =  ParseIDList(IDList,IDListSize)
    if IDs == []:
        return "Error parsing VistaAndAbove TargetLinkIDList"
    for _ID_ in IDs:
        x_x_x = _ID_.split("!!!")
        if len(x_x_x) == 4:
            Str =  ("ItemID Offset: "  + hex(int(x_x_x[0],10)))
            print Str
            FStr += (Str + "\r\n")
            
            Str = ( "ItemID Size: "  + hex(int(x_x_x[1],10)))
            print Str
            FStr += (Str + "\r\n")
            
            Str =  ( "ItemID Type: "  + x_x_x[2] )
            print Str
            FStr += (Str + "\r\n")
            
            Str = ( "ItemID Value: " + x_x_x[3] )
            print Str
            FStr += (Str + "\r\n")
            
            print "\r\n"
            Fstr +=  "\r\n"
    return FStr
    
def ParseDataBlock(DataBlock,DataBlockSize,DataBlockSignature):
    if DataBlock == "" or len(DataBlock) != DataBlockSize or IsKnownSignatureId(DataBlockSignature) == False:
        return ""
    FinalString = ""
    if DataBlockSignature == 0xA0000001:
        FinalString = ParseEnvironmentVariableDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA0000002:
        FinalString = ParseConsoleDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA0000003:
        FinalString = ParseTrackerDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA0000004:
        FinalString = ParseConsoleFEDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA0000005:
        FinalString = ParseSpecialFolderDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA0000006:
        FinalString = ParseDarwinDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA0000007:
        FinalString = ParseIconEnvironmentDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA0000008:
        FinalString = ParseShimDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA0000009:
        FinalString = ParsePropertyStoreDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA000000A: #secret one
        FinalString = "Undocumented Data Block"
    if DataBlockSignature == 0xA000000B:
        FinalString = ParseKnownFolderDataBlock(DataBlock,DataBlockSize)
    if DataBlockSignature == 0xA000000C:
       FinalString = ParseVistaAndAboveIDListDataBlock(DataBlock,DataBlockSize)
    return FinalString

    
def ParseHotKeyFlags(HotKeyFlags):
    if len(HotKeyFlags) != 2:
        return ""
    H_0 = struct.unpack("B",HotKeyFlags[0])[0]
    H_1 = struct.unpack("B",HotKeyFlags[1])[0]
    if H_0 == 0 and H_1 == 0:
        return "(empty)"
    HotKeyFlagsString = ""
    if H_1 & 1:
        HotKeyFlagsString += "Shift+"
    if H_1 & 2:
        HotKeyFlagsString += "Ctrl+"
    if H_1 & 4:
        HotKeyFlagsString += "Alt+"
    if H_1 & 4 & 0xF8:
        HotKeyFlagsString += "Unknown+"
    HotKeyFlagsString = HotKeyFlagsString.rstrip("+")
    if (H_0 >= 0x30 and H_0 <= 0x39) or (H_0 >= 0x41 and H_0 <= 0x5A):
        HotKeyFlagsString += ("+" + chr(H_0))

    if (H_0 >= 0x70 and H_0 <= 0x87):
        HotKeyFlagsString += ("+" + HotKeyFlags1Map[H_0-0x70])
    if  H_0 == 0x90:
        HotKeyFlagsString += "NUM LOCK"
    if  H_0 == 0x91:
        HotKeyFlagsString += "SCROLL LOCK"
    return HotKeyFlagsString

    
    
def PrintShowCommand(ShowCommand):
    if ShowCommand == 1:
        return "SW_SHOWNORMAL"
    elif ShowCommand == 3:
        return "SW_SHOWMAXIMIZED"
    elif ShowCommand == 7:
        return "SW_SHOWMINNOACTIVE"
    else:
        return "SW_SHOWNORMAL"
    
def PrintFileTime(FileTime):
    if len(FileTime)!=8:
        return ""
    X = struct.unpack("Q",FileTime)[0]
    XX = X / 10
    return datetime(1601,1,1) + timedelta(microseconds=XX)
    
    
def ParseFileAttributes(FileAttributes):
    if FileAttributes == "":
        return ""
    
    FileAttributesString = ""
    for i in range(0,15):
        X = 1 << i
        if FileAttributes & X:
            FileAttributesString += (FileAttributesMap[i]+"|")
    return FileAttributesString.rstrip("|")

def ParseLinkFlags(LinkFlags):
    if LinkFlags == "":
        return ""
    
    LinkFlagsString = ""
    for i in range(0,32):
        X = 1 << i
        if LinkFlags & X:
            LinkFlagsString += (LinkFlagsMap[i]+"|")
    return LinkFlagsString.rstrip("|")
    
#-------------------------------------------
#-------------------------------------------


if len(sys.argv) != 2:
    PrintFatalError("Usage: Lnk.py X.lnk\r\n",-1)

inF = sys.argv[1]
if os.path.exists(inF) == False:
    PrintFatalError("Input file does not exist\r\n",-2)



fIn = open(inF,"rb")
fCon = fIn.read()
fIn.close()

fConLen = len(fCon)
if fConLen == 0 or fConLen < 0x4C:
    PrintSmallError()

########################################################################
#Read ShellLinkHeader
HeaderSize = struct.unpack("L",fCon[0:4])[0]
if HeaderSize != 0x4C:
    PrintInvalidHeaderError()

ShellLinkHeader = fCon[0:0x4C]
LinkCLSID = ShellLinkHeader[0x4:0x14]
sLinkCLSID = PrintCLSID(LinkCLSID)
print "Link CLSID: " + sLinkCLSID + "\r\n"

LinkFlags = struct.unpack("L",ShellLinkHeader[0x14:0x18])[0]
print "Link Flags: " + hex(LinkFlags) + " (" + ParseLinkFlags(LinkFlags) + ")\r\n"


gHasLinkTargetIDList=False
gHasLinkInfo=False
gHasName=False
gHasRelativePath=False
gHasWorkingDir=False
gHasArguments=False
gHasIconLocation=False
gIsUnicode = False
gForceNoLinkInfo = False
gHasExpString = False
gRunInSeparateProcess = False
gHasDarwinID = False
gRunAsUser = False
gHasExpIcon = False
gNoPidlAlias = False
gRunWithShimLayer = False
gForceNoLinkTrack = False
gEnableTargetMetadata = False
gDisableLinkPathTracking = False
gDisableKnownFolderTracking = False
gDisableKnownFolderAlias = False
gAllowLinkToLink = False
gUnaliasOnSave = False
gPreferEnvironmentPath = False
gKeepLocalIDListForUNCTarget = False


if LinkFlags & 0x1:
    gHasLinkTargetIDList = True
if LinkFlags & 0x2:
    gHasLinkInfo = True
if LinkFlags & 0x4:
    gHasName = True
if LinkFlags & 0x8:
    gHasRelativePath = True
if LinkFlags & 0x10:
    gHasWorkingDir = True
if LinkFlags & 0x20:
    gHasArguments = True
if LinkFlags & 0x40:
    gHasIconLocation = True
if LinkFlags & 0x80:
    gIsUnicode = True

if LinkFlags & 0x100:
    gForceNoLinkInfo = False
if LinkFlags & 0x200:
    gHasExpString = False
if LinkFlags & 0x400:
    gRunInSeparateProcess = False

if LinkFlags & 0x1000:
    gHasDarwinID = False
if LinkFlags & 0x2000:
    gRunAsUser = False
if LinkFlags & 0x4000:
    gHasExpIcon = False
if LinkFlags & 0x8000:
    gNoPidlAlias = False
if LinkFlags & 0x20000:
    gRunWithShimLayer = False
if LinkFlags & 0x40000:
    gForceNoLinkTrack = False
if LinkFlags & 0x80000:
    gEnableTargetMetadata = False
if LinkFlags & 0x100000:
    gDisableLinkPathTracking = False
if LinkFlags & 0x200000:
    gDisableKnownFolderTracking = False
if LinkFlags & 0x400000:
    gDisableKnownFolderAlias = False
if LinkFlags & 0x800000:
    gAllowLinkToLink = False
if LinkFlags & 0x1000000:
    gUnaliasOnSave = False
if LinkFlags & 0x2000000:
    gPreferEnvironmentPath = False
if LinkFlags & 0x4000000:
    gKeepLocalIDListForUNCTarget = False



FileAttributes = struct.unpack("L",ShellLinkHeader[0x18:0x1C])[0]
print "Target File Attributes: " + hex(FileAttributes) + " (" + ParseFileAttributes(FileAttributes)+ ")"


CreationTime = ShellLinkHeader[0x1C:0x24]
print "Creation Time: " + str( PrintFileTime(CreationTime) )
AccessTime = ShellLinkHeader[0x24:0x2C]
print "Access Time: " + str( PrintFileTime(AccessTime) )
WriteTime = ShellLinkHeader[0x2C:0x34]
print "Write Time: " + str( PrintFileTime(WriteTime) )

FileSize = struct.unpack("L",ShellLinkHeader[0x34:0x38])[0]
print "File Size: " + str(FileSize) + " (" + hex(FileSize) + ") bytes"

IconIndex = struct.unpack("L",ShellLinkHeader[0x38:0x3C])[0]
print "Icon Index: " + hex(IconIndex)

ShowCommand = struct.unpack("L",ShellLinkHeader[0x3C:0x40])[0]
print "ShowCommand: " + PrintShowCommand(IconIndex)

HotKeyFlags = ShellLinkHeader[0x40:0x42]
print "HotKey flags: " + ParseHotKeyFlags(HotKeyFlags)

Reserved1 = ShellLinkHeader[0x42:0x44]
Reserved2 = ShellLinkHeader[0x44:0x48]
Reserved3 = ShellLinkHeader[0x48:0x4C]

########################################################################
#Read LinkTargetIDList
Next = 0x4C
if gHasLinkTargetIDList == True:
    print "\r\n=========== \r\nNow parsing TargetLinkIDList\r\n"
    if fConLen < Next+2:
        PrintSmallError()
    IDListSize = struct.unpack("H",fCon[Next:Next+0x2])[0]
    if  Next + IDListSize > fConLen:
        PrintSmallError()
    print "IDListSize: " + hex(IDListSize) + "\r\n"
    Next += 2
    IDList = fCon[Next:Next+IDListSize]
    IDs =  ParseIDList(IDList,IDListSize)
    if IDs == []:
        PrintFatalError("Error parsing TargetLinkIDList\r\n",-6)
    #print IDs
    for _ID_ in IDs:
        x_x_x = _ID_.split("!!!")
        if len(x_x_x) == 4:
            print "ItemID Offset: "  + hex(int(x_x_x[0],10))
            print "ItemID Size: "  + hex(int(x_x_x[1],10))
            print "ItemID Type: "  + x_x_x[2]
            print "ItemID Value: " + x_x_x[3]
            print "\r\n"
    Next += IDListSize
########################################################################
#Read LinkInfo 
if gHasLinkInfo == True:
    print "\r\n=========== \r\nNow parsing LinkInfo\r\n"
    if fConLen < Next+4:
        PrintSmallError()
    LinkInfoSize = struct.unpack("L",fCon[Next:Next+0x4])[0]
    #print hex(Next)
    #print hex(LinkInfoSize)
    if fConLen < Next + LinkInfoSize:
        PrintSmallError()
    LinkInfo = fCon[Next:Next+LinkInfoSize]
    Next += LinkInfoSize
    LinkInfoHeaderSize = struct.unpack("L",LinkInfo[4:8])[0]
    if LinkInfoHeaderSize >= LinkInfoSize:
        PrintSmallError()
    LinkInfoHeader = LinkInfo[0:LinkInfoHeaderSize]
    ret = ParseLinkInfo(LinkInfo,LinkInfoSize,LinkInfoHeader,LinkInfoHeaderSize)
    #print ret
    if ret == []:
        print "Empty LinkInfo section\r\n"
    else:
        for _ret_ in ret:
            if _ret_ != {}:
                if _ret_["Type"]!="":
                    if _ret_["Type"] == "Volume":
                        print "== Volume ==>\r\n"
                        if _ret_["DriveType"] != "":
                            xDT = _ret_["DriveType"]
                            print "Drive Type: " + hex(xDT) + " (" + GetDriveTypeString(xDT) +")"
                        if _ret_["VolumeA"] != "":
                            print "Drive Name: " + _ret_["VolumeA"]
                        if _ret_["VolumeU"] != "":
                            print "Drive Name: " + _ret_["VolumeA"]
                        if _ret_["DriveSerialNumber"] != "":
                            xDSN = _ret_["DriveSerialNumber"]
                            print "Drive SerialNo: " + hex(xDSN) + " (" + PrintDriveSerialNumber(xDSN) + ")"
                    elif _ret_["Type"] == "LocalBasePath":
                        print "== LocalBasePath ==>\r\n"
                        if _ret_["LocalBasePathA"] != "":
                            print "LocalBasePath: " + _ret_["LocalBasePathA"]
                        if _ret_["LocalBasePathU"] != "":
                            print "LocalBasePath: " + _ret_["LocalBasePathU"]
                    elif _ret_["Type"] == "CommonNetworkRelativeLink":
                        print "== CommonNetworkRelativeLink ==>\r\n"
                        if _ret_["NetworkProviderType"] != 0:
                            print "Network Provider: " + GetNetworkProviderString(NetworkProviderType)
                        if _ret_["NetNameA"] != "":
                            print "NetName: " + _ret_["NetNameA"]
                        if _ret_["NetNameU"] != "":
                            print "NetName: " + _ret_["NetNameU"]
                        if _ret_["DeviceNameA"] != "":
                            print "DeviceName: " + _ret_["DeviceNameA"]
                        if _ret_["DeviceNameU"] != "":
                            print "DeviceName: " + _ret_["DeviceNameU"]
                    elif _ret_["Type"] == "CommonPathSuffix":
                        print "== CommonPathSuffix ==>\r\n"
                        if _ret_["CommonPathSuffixU"] != "":
                            print "CommonPathSuffix: " + _ret_["CommonPathSuffixU"]
                        if _ret_["CommonPathSuffixA"] != "":
                            print "CommonPathSuffix: " + _ret_["CommonPathSuffixA"]
                    else:
                        print "Unsupported"
########################################################################
#Read StringData


if fConLen < Next + 2:
    PrintSmallError()
print "\r\n=========== \r\nNow parsing StringData\r\n"

Name = ""  
if gHasName == True:
        #Read Name (Description string)
        NameLenX = struct.unpack("H",fCon[Next:Next+2])[0]
            
        Next += 2

        if gIsUnicode == True:
            NameLenX += NameLenX
        
        if fConLen < Next + NameLenX:
            PrintSmallError()
        
        NameX = fCon[Next:Next+NameLenX]
        Next += NameLenX
        
        if gIsUnicode == False:
            Name = NameX
        else:
            Name = NameX.decode("utf-16").encode("utf-8")
        print "Name: " + Name
        
            
#Read RelativePath
if fConLen < Next + 2:
    PrintSmallError()

RelativePath = ""  
if gHasRelativePath == True:
        
        RelativePathLenX = struct.unpack("H",fCon[Next:Next+2])[0]
            
        Next += 2

        if gIsUnicode == True:
            RelativePathLenX += RelativePathLenX
        #print hex(RelativePathLenX)
        if fConLen < Next + RelativePathLenX:
            PrintSmallError()
        
        RelativePathX = fCon[Next:Next+RelativePathLenX]
        Next += RelativePathLenX

        if gIsUnicode == False:
            RelativePath = RelativePathX
        else:
            RelativePath = RelativePathX.decode("utf-16").encode("utf-8")
        print "Relative Path: " + RelativePath 
        

#Read WorkingDir
if fConLen < Next + 2:
    PrintSmallError()

WorkingDir = ""  
if gHasWorkingDir == True:
        
        WorkingDirLenX = struct.unpack("H",fCon[Next:Next+2])[0]
            
        Next += 2

        if gIsUnicode == True:
            WorkingDirLenX += WorkingDirLenX
        #print hex(RelativePathLenX)
        if fConLen < Next + WorkingDirLenX:
            PrintSmallError()
        
        WorkingDirX = fCon[Next:Next+WorkingDirLenX]
        Next += WorkingDirLenX

        if gIsUnicode == False:
            WorkingDir = WorkingDirX
        else:
            WorkingDir = WorkingDirX.decode("utf-16").encode("utf-8")
        print "Working Dir: " + WorkingDir 
    

#Read Arguments
if fConLen < Next + 2:
    PrintSmallError()

Arguments = ""  
if gHasArguments == True:
        
        ArgumentsLenX = struct.unpack("H",fCon[Next:Next+2])[0]
            
        Next += 2

        if gIsUnicode == True:
            ArgumentsLenX += ArgumentsLenX

        if fConLen < Next + ArgumentsLenX:
            PrintSmallError()
        
        ArgumentsX = fCon[Next:Next+ArgumentsLenX]
        Next += ArgumentsLenX

        if gIsUnicode == False:
            Arguments = ArgumentsX
        else:
            Arguments = ArgumentsX.decode("utf-16").encode("utf-8")
        print "Arguments: " + Arguments

#Read IconLocation
if fConLen < Next + 2:
    PrintSmallError()

IconLocation = ""  
if gHasIconLocation == True:
        
        IconLocationLenX = struct.unpack("H",fCon[Next:Next+2])[0]
            
        Next += 2

        if gIsUnicode == True:
            IconLocationLenX += IconLocationLenX

        if fConLen < Next + IconLocationLenX:
            PrintSmallError()
        
        IconLocationX = fCon[Next:Next+IconLocationLenX]
        Next += IconLocationLenX

        if gIsUnicode == False:
            IconLocation = IconLocationX
        else:
            IconLocation = IconLocationX.decode("utf-16").encode("utf-8")
        print "IconLocation: " + IconLocation

########################################################################
#Read ExtraData
print "\r\n=========== \r\nNow parsing ExtraData\r\n"
TerminalBlockFound = False

BlockNum = 0
while TerminalBlockFound == False:
    #print "Next: " + hex(Next)
    if fConLen < Next + 4:
        PrintSmallError()
    BlockSize = struct.unpack("L",fCon[Next:Next+4])[0]
    #print "Block Size: " + hex(BlockSize)
    #Check for Terminal Block
    if BlockSize == 0:
        TerminalBlockFound = True
        print "Terminal Block found\r\n"
        break
    print "DataBlock No. ===> " + str(BlockNum)
    if fConLen < Next + BlockSize:
        PrintSmallError()
    
    BlockSignature = struct.unpack("L",fCon[Next+4:Next+8])[0]
    print "Block Signaure: " + hex(BlockSignature) + " (" + GetNameFromSignatureId(BlockSignature) + ")"
    #print GetNameFromSignatureId(BlockSignature)

    DataBlock = fCon[Next:Next+BlockSize]
    ret = ParseDataBlock(DataBlock,BlockSize,BlockSignature)
    
    Next += BlockSize
    BlockNum += 1




if TerminalBlockFound == True:
    print "Done successfully\r\n"
sys.exit(0)
