from search_service import search_regulations

query = "Customer consent before processing data"

results = search_regulations(query)

for result in results:

    print("="*60)

    print(result["id"])

    print(result["law"])

    print(result["country"])

    print(result["risk"])

    print(result["text"])