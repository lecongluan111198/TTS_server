import torchaudio
import time
from pydub import AudioSegment
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN
from concurrent.futures import ThreadPoolExecutor, as_completed

class Tacotron2:
    tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")

    def text_to_spec(self, text):
        mel_output, mel_length, alignment = Tacotron2.tacotron2.encode_text(text)
        return mel_output

    def spec_to_wave_form(self, mel_spec):
        waveforms = Tacotron2.hifi_gan.decode_batch(mel_spec)
        return waveforms

    def to_wave_form(self, text, index=0):
        mel_spec = self.text_to_spec(text)
        wave = self.spec_to_wave_form(mel_spec)
        file = f'resource/{index}_{current_milli_time()}.wav'
        torchaudio.save(file, wave.squeeze(1), 22050)
        AudioSegment.from_wav(file).export(file.replace("wav", "mp3"), format="mp3")
        return file.replace("wav", "mp3"), index

executor = ThreadPoolExecutor(5)
tts_model = Tacotron2()

def current_milli_time():
    return round(time.time() * 1000)

def to_wave_form_with_multi_texts(texts):
    ret = [""] * len(texts)
    futures = {executor.submit(tts_model.to_wave_form, text.strip(), i):  (i, text) for i, text in enumerate(texts)}
    for future in as_completed(futures):
        text1, text2 = futures[future]
        try:
            source, i = future.result()
            ret[i] = {"src": source, "sentence": text2}
        except Exception as exc:
            print('%r generated an exception: %s' % (text, exc))
    return ret

    

