import torchaudio
import time
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN


def current_milli_time():
    return round(time.time() * 1000)

class Tacotron2:
    tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")

    def text_to_spec(self, text):
        mel_output, mel_length, alignment = Tacotron2.tacotron2.encode_text(text)
        return mel_output

    def spec_to_wave_form(self, mel_spec):
        waveforms = Tacotron2.hifi_gan.decode_batch(mel_spec)
        return waveforms

    def to_wave_form(self, text):
        mel_spec = self.text_to_spec(text)
        wave = self.spec_to_wave_form(mel_spec)
        torchaudio.save(f'resource/{current_milli_time()}.wav', wave.squeeze(1), 22050)
        return f'{current_milli_time()}.wav'
