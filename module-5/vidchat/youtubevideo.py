class YoutubeVideo():

    def __init__ (self, video_id, video_title, video_url, channel_name, duration, publish_date):

        self.video_id = video_id,
        self.video_title = video_title
        self.video_url = video_url
        self.channel_name = channel_name
        self.duration = duration
        self.publish_date = publish_date

        #örnek alırken bu özelliklerin hepsinin doldurulmasını sağlayacak atama kısmı tamamlandı. örneğin video_id
        #parametresine verilen değerin bu sınıfın o spesifik örneği için hafızada tutulmasını sağlıyoruz.

