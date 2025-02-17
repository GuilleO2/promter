"""Módulo para grabar audio"""
import pyaudio
import wave
import os
from datetime import datetime
import config

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False
        self.current_file = None
        
    def start_recording(self, filename=None):
        """Inicia la grabación de audio"""
        if self.recording:
            return
            
        # Si no se proporciona un nombre de archivo, crear uno con timestamp
        if filename is None:
            if not os.path.exists(config.RECORDINGS_DIR):
                os.makedirs(config.RECORDINGS_DIR)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(config.RECORDINGS_DIR, f'recording_{timestamp}.wav')
            
        self.current_file = filename
        self.frames = []
        self.recording = True
        
        # Configuración de la grabación
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=config.AUDIO_CHANNELS,
            rate=config.AUDIO_RATE,
            input=True,
            frames_per_buffer=config.AUDIO_CHUNK,
            stream_callback=self._callback
        )
        self.stream.start_stream()
        
    def stop_recording(self):
        """Detiene la grabación y guarda el archivo"""
        if not self.recording:
            return None
            
        self.recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(self.current_file), exist_ok=True)
            
        # Guardar el archivo
        if self.frames and self.current_file:
            wf = wave.open(self.current_file, 'wb')
            wf.setnchannels(config.AUDIO_CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(config.AUDIO_RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            return self.current_file
            
        return None
        
    def _callback(self, in_data, frame_count, time_info, status):
        """Callback para procesar los datos de audio"""
        if self.recording:
            self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)
        
    def __del__(self):
        """Limpieza al destruir el objeto"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
