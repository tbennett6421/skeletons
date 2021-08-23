# Module arguments
__code_debug__ = False

# Base Imports
from maltego_trx.maltego import UIM_INFORM
from maltego_trx.transform import DiscoverableTransform

class SplitEmailAddress(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        """ Maltego Transform Entrypoint """
        # get request criteria
        email = request.Value
        email_user, email_domain = email.split("@")
        response.addEntity("availity.identity.emailusername", str(email_user))
        response.addEntity("availity.identity.emaildomain", str(email_domain))

if __name__ == "__main__":
    pass
