from main_langchain import ask
def test_full_time_vacation():
    answer = ask("How many vacation days do I get as a full time employee?")
    assert "15" in answer

def test_I_dont_know():
    answer = ask("Do I get salary hike this year?")
    assert "I don't know" in answer

def test_contractor():
    answer = ask("How many vacation days do I get as a contractor?")
    assert "not eligible" in answer

def test_parttime():
    answer = ask("How many vacation days do I get as a parttime worker?")
    assert "8" in answer

def test_contract():
    answer = ask("How many sick days do I get as a contractor?")
    assert "I don't know" in answer