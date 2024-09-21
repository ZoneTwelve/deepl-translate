from deepl.hacks import generate_timestamp
from deepl.settings import MAGIC_NUMBER, SUPPORTED_FORMALITY_TONES

from typing import Union

def generate_split_sentences_request_data(text, identifier=MAGIC_NUMBER, **kwargs):
    return {
        "jsonrpc": "2.0",
        "method": "LMT_split_into_sentences",
        "params": {
            "texts": [text],
            "lang": {"lang_user_selected": "auto", "user_preferred_langs": []},
        },
        "id": identifier,
    }


def generate_jobs(sentences, beams=1):
    jobs = []
    for idx, sentence in enumerate(sentences):
        job = {
            "kind": "default",
            "raw_en_sentence": sentence,
            "raw_en_context_before": sentences[:idx],
            "raw_en_context_after": [sentences[idx + 1]]
            if idx + 1 < len(sentences)
            else [],
            "preferred_num_beams": beams,
        }
        jobs.append(job)
    return jobs


def generate_common_job_params(formality_tone, target_language: Union[dict, str] = {}):
    """
    "commonJobParams": {
      "quality": "normal",
      "regionalVariant": "zh-Hant",
      "mode": "translate",
      "browserType": 1,
      "textType": "plaintext"
    },
    """
    ret = {}

    # Extract regional variant if available
    if isinstance(target_language, dict) and 'config' in target_language:
        ret['regionalVariant'] = target_language['config'].get('regionalVariant')

    # Handle formality tone
    if formality_tone is not None:
        if formality_tone in SUPPORTED_FORMALITY_TONES:
            ret['formality'] = formality_tone
        else:
            raise ValueError(f"Formality tone '{formality_tone}' not supported. "
                             f"Supported tones are: {', '.join(SUPPORTED_FORMALITY_TONES)}")

    return ret

def generate_translation_request_data(
    source_language: Union[str, dict],
    target_language: Union[str, dict],
    sentences,
    identifier=MAGIC_NUMBER,
    alternatives=1,
    formality_tone=None,
):
    if isinstance(source_language, dict):
        source_language_code = source_language['config']['code']
    else:
        source_language_code = source_language
    if isinstance(target_language, dict):
        target_language_code = target_language['config']['code']
    else:
        target_language_code = target_language
    ret = {
        "jsonrpc": "2.0",
        "method": "LMT_handle_jobs",
        "params": {
            "jobs": generate_jobs(sentences, beams=alternatives),
            "lang": {
                "user_preferred_langs": [target_language_code, source_language_code],
                "source_lang_computed": source_language_code,
                "target_lang": target_language_code,
            },
            "priority": 1,
            "commonJobParams": generate_common_job_params(formality_tone, target_language),
            "timestamp": generate_timestamp(sentences),
        },
        "id": identifier,
    }
    # print(ret)
    return ret
