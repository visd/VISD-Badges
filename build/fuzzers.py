import random
import string

import names

from factory import fuzzy

from django.contrib.auth.models import User, Group


class FishFuzz(fuzzy.BaseFuzzyAttribute):

    def __init__(self, low, high, **kwargs):
        
        self.low = low
        self.high = high

        super(FishFuzz, self).__init__(**kwargs)

    def fuzz(self):
        tunatext = 'swallower tadpole cod clingfish billfish mud catfish soapfish damselfish whitefish soldierfish whitebait lumpsucker hussar splitfin rough pomfret flagfin northern pike vimba wrymouth trumpeter righteye flounder combtail gourami sand goby ghost fish gray mullet plunderfish marlin spiny eel sea snail false cat shark half-gill sea bass butterflyfish dottyback trumpeter deep sea anglerfish shrimpfish sand knifefish largenose fish sand knifefish mudskipper herring smelt cornish spaktailed bream unicorn fish danio thresher shark dartfish shortnose sucker spearfish coffinfish rock bass marine hatchetfish guppy huchen spanish mackerel sawtooth eel angler french angelfish oldwife shortnose sucker pencil catfish warbonnet mola scat codling kelp perch wolf-herring whiptail gulper buri icefish ribbonbearer regal whiptail catfish smooth dogfish tadpole cod peladillo amur pike shad south american lungfish skilfish pacific herring zebra oto loach basking shark grunter mola mola sunfish thornfish blenny tarpon combtail gourami redhorse sucker pupfish sleeper pencil catfish burrowing goby mosshead warbonnet sixgill ray opaleye louvar sand tiger ruffe tench herring grideye ribbonfish eagle ray whitefish rock bass american sole shell-ear loach catfish peamouth shad trumpetfish rainbowfish bonytongue silver hake mullet dartfish rabbitfish sand eel tench european eel mexican golden trout longnose dace kelp perch angler catfish dorado yellowtail amberjack marlin yellow-edged moray roanoke bass grunt sculpin green swordtail australian lungfish atlantic silverside plownose chimaera zebra pleco sand goby porgy shark clown loach cuckoo wrasse mooneye black scalyfin surf sardine pricklefish swordfish halosaur suckermouth armored catfish molly blind shark saury slickhead pike conger cornish spaktailed bream crestfish plownose chimaera largemouth bass coffinfish blue gourami javelin swordfish loweye catfish sillago treefish morid cod hammerhead shark tonguefish denticle herring amur pike redfish jack dempsey death valley pupfish cherry salmon mexican golden trout bigscale fish snake eel grenadier longfin smelt ratfish taimen orangestriped triggerfish haddock red snapper char pacific salmon surf sardine skipjack tuna angler australian herring threespine stickleback kissing gourami trahira ground shark common tunny southern dolly varden tenpounder paddlefish sailfish blue shark pelagic cod ground shark mosquitofish southern grayling mummichog angler tiger shark garden eel hairtail gray eel-catfish yellowfin croaker dragonet tubeblenny golden trout tonguefish bigscale pomfret tubeshoulder sharksucker surgeonfish walleye pollock snake mackerel seahorse green swordtail sabalo blue shark ocean perch moorish idol yellow weaver brook lamprey darter black swallower sand knifefish'

        phrase_list = []
        word_list = tunatext.split()
        for _ in range(random.randint(self.low,self.high)):
            word_index = random.randint(0, len(word_list) - 1)
            phrase_list.append(word_list[word_index])
        return ' '.join(phrase_list)


class HexFuzz(fuzzy.BaseFuzzyAttribute):

    def fuzz(self):
        return hex(random.randint(1000,100000))


class SlugFuzz(fuzzy.BaseFuzzyAttribute):
    """ Returns a random slug of random length from 3 to 10
    """

    def fuzz(self):
        return ''.join(random.choice(string.lowercase) for i in range(random.randint(3,10)))


class FirstNameFuzz(fuzzy.BaseFuzzyAttribute):
    """ Returns a first name, from the names module.
    """

    def fuzz(self):
        return names.get_first_name()


class LastNameFuzz(fuzzy.BaseFuzzyAttribute):
    """ Returns a last name, from the names module.
    """

    def fuzz(self):
        return names.get_last_name()


class RandomExistingUser(fuzzy.BaseFuzzyAttribute):

    def fuzz(self):
        return User.objects.order_by('?')[0]

class RandomGroupAndChildren(fuzzy.BaseFuzzyAttribute):

    def fuzz(self):
        from permits.methods import get_child_groups
        group = Group.objects.order_by('?')[0]
        allgroups = get_child_groups(group.name)
        allgroups.append(group.name)
        return allgroups