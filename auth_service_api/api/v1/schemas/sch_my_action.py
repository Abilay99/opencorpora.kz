from auth_service_api.extensions import ma
class ResMyActionSchema(ma.Schema):
    ServiceName = ma.Str()
    RequestId = ma.Str()
    StatusAppeals = ma.Boolean()
    DateTimeStatement = ma.Str()
    StatusRecived = ma.Str()
    ReceivedTime = ma.Str()
    ResultTiming = ma.Int(required=True)
    DatatimeOfTheResult = ma.Str()
    StatusApplication = ma.Str()
