import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load(r'clip\noisy\p257_089_mic1.flac', sr=None)

fig, ax = plt.subplots(2, 1, figsize=(12, 8),
                      gridspec_kw={
                          'hspace': 0,
                          'height_ratios': [5, 8]
                      })


# -----------------------------------------
ax[0].plot(np.linspace(0, len(y)/sr, len(y)), y, linewidth=0.25, color=(160/255, 60/255, 200/255))
ax[0].set_ylabel('Amplitude', labelpad=10)
ax[0].set_ylim(-1, 1)
ax[0].set_xlim(0, len(y)/sr)
ax[0].grid(True, alpha=0.3)
ax[0].set_xticklabels([])
ax[0].axis('off') 

# -----------------------------------------
D = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=256)), ref=1.0)

librosa.display.specshow(D, sr=sr, hop_length=256,
                        x_axis='time', y_axis='hz', 
                        ax=ax[1], cmap='magma',
                        vmin=-46.4743, vmax=50.0460)


ax[1].set_ylabel('Frequency (Hz)', labelpad=10)
ax[1].set_ylim(0, sr//2)
ax[1].tick_params(axis='y', which='major', length=3, pad=2)
ax[1].grid(True, axis='y', alpha=0.3)
ax[1].axis('off') 


for a in ax:
    a.set_xlabel('Time (s)', labelpad=8) if a == ax[1] else None
    a.tick_params(axis='x', which='both', length=3, pad=2)

# plt.tight_layout()
# plt.show()
plt.savefig('output.png', bbox_inches='tight', pad_inches=0, dpi=300)