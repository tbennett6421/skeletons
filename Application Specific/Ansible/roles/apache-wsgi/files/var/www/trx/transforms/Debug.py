from maltego_trx.entities import Person,Domain,Phrase
from maltego_trx.maltego import UIM_PARTIAL
from maltego_trx.transform import DiscoverableTransform

class Debug(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        maltego_t = request.Type
        maltego_v = request.Value
        maltego_w = request.Weight
        maltego_s = request.Slider
        maltego_props = request.Properties
        maltego_trans = request.TransformSettings
        response.addEntity(Phrase, "Type: "+str(maltego_t))
        response.addEntity(Phrase, "Value: "+str(maltego_v))
        response.addEntity(Phrase, "Weight: "+str(maltego_w))
        response.addEntity(Phrase, "Slider: "+str(maltego_s))
        i=0
        for k,v in maltego_props.items():
            response.addEntity(Phrase, "Maltego Properties: Index[%d]::Key[%s] => Val [%s] " % (i, str(k), str(v)) )
            i=i+1
        i=0
        for k,v in maltego_trans.items():
            response.addEntity(Phrase, "Maltego Transform Settings: Index[%d]::Key[%s] => Val [%s] " % (i, str(k), str(v)) )
            i=i+1

if __name__ == "__main__":
    pass
