import torchaudio
import time
from pydub import AudioSegment
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

    def to_wave_form(self, text, index=0):
        mel_spec = self.text_to_spec(text)
        wave = self.spec_to_wave_form(mel_spec)
        file = f'resource/{index}_{current_milli_time()}.wav'
        torchaudio.save(file, wave.squeeze(1), 22050)
        AudioSegment.from_wav(file).export(file.replace("wav", "mp3"), format="mp3")
        return file.replace("wav", "mp3")
