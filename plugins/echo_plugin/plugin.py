def run(input_data):
    print("🔧 [echo plugin] received:")
    print(input_data)
    return {"status": "ok", "input": input_data}
