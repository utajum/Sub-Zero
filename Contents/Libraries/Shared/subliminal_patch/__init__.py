# coding=utf-8

import subliminal
import babelfish

from .patch_provider_pool import PatchedProviderPool
from .patch_video import patched_search_external_subtitles, scan_video
from .patch_providers import addic7ed, podnapisi, tvsubtitles, opensubtitles


# patch subliminal's ProviderPool 
subliminal.api.ProviderPool = PatchedProviderPool

# patch subliminal's subtitle classes
def subtitleRepr(self):
    link = self.page_link

    # specialcasing addic7ed; eww
    if self.__class__.__name__ == "Addic7edSubtitle":
	link = u"http://www.addic7ed.com/%s" % self.download_link
    return '<%s %r [%s]>' % (self.__class__.__name__, link, self.language)

subliminal.subtitle.Subtitle.__repr__ = subtitleRepr

# patch subliminal's providers
subliminal.providers.addic7ed.Addic7edProvider = addic7ed.PatchedAddic7edProvider
subliminal.providers.podnapisi.PodnapisiProvider = podnapisi.PatchedPodnapisiProvider
subliminal.providers.tvsubtitles.TVsubtitlesProvider = tvsubtitles.PatchedTVsubtitlesProvider
subliminal.providers.opensubtitles.OpenSubtitlesProvider = opensubtitles.PatchedOpenSubtitlesProvider



# add language converters
babelfish.language_converters.register('addic7ed = subliminal_patch.patch_language:PatchedAddic7edConverter')
babelfish.language_converters.register('tvsubtitles = subliminal.converters.tvsubtitles:TVsubtitlesConverter')

# patch subliminal's external subtitles search algorithm
subliminal.video.search_external_subtitles = patched_search_external_subtitles

# patch subliminal's scan_video function
subliminal.video.scan_video = scan_video

subliminal.video.Episode.scores["boost"] = 40