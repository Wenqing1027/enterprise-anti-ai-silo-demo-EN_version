# App Pairing Failure Troubleshooting (Synthetic)

## Common causes
1. Vehicle 4G not activated or connectivity service expired;
2. Phone Bluetooth/location permissions not enabled;
3. Factory binding from store not released;
4. Non-smart vehicle mistakenly routed through smart-vehicle pairing flow.

## Process
1. Look up VIN and confirm whether it is a smart vehicle;
2. Check renewal pool: if service expired, guide renewal before pairing;
3. Trigger backend "force unpair (store verification code required)";
4. Guide user to retry within 2 meters with App in foreground.

## Related tags
- Software/account-related failure: mark "pairing failure"
- User upset and repeat calls: assess whether to mark "open complaint"

Do not promise "it must be a software issue"—rule out hardware antenna and network coverage first.
