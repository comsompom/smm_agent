import os
import torch


device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'

current_model = "https://models.silero.ai/models/tts/en/v3_en.pt"  # en speaker model
# current_model = "https://models.silero.ai/models/tts/ru/v4_ru.pt"  # rus speakers model


if not os.path.isfile(local_file):
    torch.hub.download_url_to_file(current_model,
                                   local_file)

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)

example_text = """
well, The future isn't just arriving; it's being built, 
piece by lunar piece. Imagine securing your legacy, not 
just on Earth, but among the stars. Investing in the Moon 
is more than a financial decision; it's a monumental leap 
into the next trillion-dollar economy, offering unparalleled 
growth potential and pioneering advantage. This isn't merely 
an investment; it's your definitive stake in humanity's most 
ambitious endeavor.
Join the visionary few who see beyond the horizon, 
who understand that true wealth lies in shaping the future. 
Embrace the opportunity to be part of an interstellar revolution, 
where your capital fuels innovation and establishes a new 
frontier for generations. This is the ultimate investment for 
those who dare to dream big and build bigger. Secure your place 
in the lunar future today. ok
"""

sample_rate = 48000
'''
rus speakers:
aidar, baya, kseniya, xenia, eugene

english speakers:
should be in en_0, en_1, en_2, en_3, en_4, en_5, en_6, en_7, en_8, 
en_9, en_10, en_11, en_12, en_13, en_14, en_15, en_16, en_17, en_18, 
en_19, en_20, en_21, en_22, en_23, en_24, en_25, en_26, en_27, en_28, 
en_29, en_30, en_31, en_32, en_33, en_34, en_35, en_36, en_37, en_38, 
en_39, en_40, en_41, en_42, en_43, en_44, en_45, en_46, en_47, en_48, 
en_49, en_50, en_51, en_52, en_53, en_54, en_55, en_56, en_57, en_58, 
en_59, en_60, en_61, en_62, en_63, en_64, en_65, en_66, en_67, en_68, 
en_69, en_70, en_71, en_72, en_73, en_74, en_75, en_76, en_77, en_78, 
en_79, en_80, en_81, en_82, en_83, en_84, en_85, en_86, en_87, en_88, 
en_89, en_90, en_91, en_92, en_93, en_94, en_95, en_96, en_97, en_98, 
en_99, en_100, en_101, en_102, en_103, en_104, en_105, en_106, 
en_107, en_108, en_109, en_110, en_111, en_112, en_113, en_114, 
en_115, en_116, en_117, random
'''
speaker = 'en_30'

audio_paths = model.save_wav(text=example_text,
                             speaker=speaker,
                             sample_rate=sample_rate)
