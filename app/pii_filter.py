from langdetect import detect
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider

# language detection
def detect_language(text: str) -> str:
    try:
        language = detect(text)
        if language not in ["en", "de"]:
            return "en"  # Default to English if language is unsupported
        return language
    except:
        return "en"  # Default to English in case of detection failure

def create_analyzer():
    # Define the NLP engine configuration
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {"lang_code": "de", "model_name": "de_core_news_lg"},
            {"lang_code": "en", "model_name": "en_core_web_lg"}
        ]
    }

    # Create the NLP engine using the provider
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()

    # Load the recognizer registry
    registry = RecognizerRegistry()
    registry.load_predefined_recognizers(nlp_engine=nlp_engine, languages=["en", "de"])
    registry.supported_languages = ["en", "de"]

    # Define a regex pattern for international phone numbers
    phone_pattern = Pattern(
        name="international_phone_pattern",
        regex=r"\+?\d[\d\s\-()]{7,}\d",
        score=0.8
    )

    # Create a custom phone number recognizer for English
    phone_recognizer_en = PatternRecognizer(
        supported_entity="PHONE_NUMBER",
        patterns=[phone_pattern],
        supported_language="en"
    )

    # Create a custom phone number recognizer for German
    phone_recognizer_de = PatternRecognizer(
        supported_entity="PHONE_NUMBER",
        patterns=[phone_pattern],
        supported_language="de"
    )

    # Add the custom recognizers to the registry
    registry.add_recognizer(phone_recognizer_en)
    registry.add_recognizer(phone_recognizer_de)

    # Create the analyzer engine with the NLP engine and registry
    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine,
        registry=registry,
        supported_languages=["en", "de"]
    )

    return analyzer


def redact_pii(text: str, analyzer: AnalyzerEngine) -> str:
    # Detect the language of the input text
    language = detect_language(text)

    entities = ["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD", "LOCATION"]
    results = analyzer.analyze(text=text, language=language)

    redacted_text = text
    offset = 0
    for result in sorted(results, key=lambda x: x.start):
        if result.entity_type in entities:
            start, end = result.start + offset, result.end + offset
            redacted_text = redacted_text[:start] + "[REDACTED]" + redacted_text[end:]
            offset += len("[REDACTED]") - (end - start)

    return redacted_text

