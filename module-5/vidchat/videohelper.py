import scrapetube
from langchain_community.document_loaders.generic import GenericLoader
# youtubeaudioloader ve openaiwhisperparser'i birbiri ile ilişkilendirmek için
from langchain_community.document_loaders import YoutubeAudioLoader
# youtubedan ses çekmek için
from langchain_community.document_loaders.parsers import OpenAIWhisperParser
# çektiğimiz sesi transkripte dönüştürür

import os
from dotenv import load_dotenv

from youtubevideo import YoutubeVideo

load_dotenv()

my_key_openai = os.getenv("openai_apikey")

#Transkripsiyon
def get_video_transcript(url):

    target_dir = "./audios/"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    loader = GenericLoader(
        YoutubeAudioLoader(urls=[url],save_dir=target_dir),
        OpenAIWhisperParser(api_key=my_key_openai)
    )
    #youtubedan yükleme yapabilen loaderim var.

    video_transcript_docs = loader.load()

    return video_transcript_docs


#Youtube Araması

def get_videos_for_search_term(search_term,video_count=1,sorting_criteria="relevance"):

    #scrapetube.get_search() metodu ile ingilizce keyler gördüğümüz ve tr görmek için:

    convert_sorting_option = {
        "En İlgili": "relevance",
        "Tarihe Göre": "upload_date",
        "İzlenme Sayısı": "view_count",
        "Beğeni Sayısı": "rating"
    }

    videos = scrapetube.get_search(query=search_term,limit=video_count,sort_by=convert_sorting_option[sorting_criteria])

    videolist = list(videos)

    # youtube arama sonucu elde ettiğimiz videolar bir liste olarak tutuldu.bu videolar ile ilgili çok fazla bilgi
    # var bunları yönetmek için 2.python dosyasını burada kullanacağız. (youtubevideo)
    #youtubevideo: bizim veri modelimiz olacak. listedeki her elemanı standart bir veri modeli ile temsil edebilmek
    # için, hepsini kolaylıkla okuyup yazabilmek için oluşturacağız.

    youtube_videos = []

    for video in videolist:
        new_video = YoutubeVideo(
            video_id=video["videoId"],
            video_title=video["title"]["runs"][0]["text"],
            video_url="https://www.youtube.com/watch?v=" + video["videoId"],
            channel_name=video["longBylineText"]["runs"][0]["text"],
            duration=video["lengthText"]["accessibility"]["accessibilityData"]["label"],
            publish_date=video["publishedTimeText"]["simpleText"]
        )

        youtube_videos.append(new_video)

        return youtube_videos
