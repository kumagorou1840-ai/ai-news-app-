import React, { useState } from 'react';
import { newsDatabase, NewsItem, NewsletterType } from './data/newsDatabase';
import './styles/newsletter.css';
import { Share2, Mail, ExternalLink, ArrowLeft, Newspaper, Bot, Calendar } from 'lucide-react';

const Header: React.FC<{ type: NewsletterType; date: string }> = ({ type, date }) => {
  const title = type === 'general' ? 'AI News Daily' : 'AI Agents Daily';
  
  // 日付の表示形式を整える
  const formattedDate = new Date(date).toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });

  return (
    <header className="header">
      <h1>{title}</h1>
      <div className="header-meta">
        <span>第 {date.replace(/-/g, '')} 号</span>
        <span>{formattedDate}</span>
        <span>編集：よっちゃん</span>
      </div>
    </header>
  );
};

const NewsItemCard: React.FC<{ item: NewsItem; index: number; onReadMore: (item: NewsItem) => void }> = ({ item, index, onReadMore }) => {
  return (
    <div className="news-item">
      <span className="news-number">{index + 1}</span>
      <span className="news-category">{item.category}</span>
      <h3 className="news-title">{item.title}</h3>
      <p className="news-summary">{item.summary}</p>
      <div className="news-footer">
        <span className="news-source">{item.source} 経由</span>
        <button onClick={() => onReadMore(item)} className="read-more-btn">記事全文を読む &rarr;</button>
      </div>
    </div>
  );
};

const NewsDetail: React.FC<{ item: NewsItem; date: string; onBack: () => void }> = ({ item, date, onBack }) => {
  const formattedDate = new Date(date).toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <div className="news-detail">
      <button onClick={onBack} className="back-btn">
        <ArrowLeft size={18} /> 一覧に戻る
      </button>
      <span className="news-category">{item.category}</span>
      <h2 className="detail-title">{item.title}</h2>
      <div className="detail-meta">
        <span>ソース: {item.source}</span>
        <span>公開日: {formattedDate}</span>
      </div>
      <div className="detail-content">
        <p>{item.fullContent}</p>
      </div>
      <div className="detail-footer">
        <p>この記事をシェアする</p>
        <div style={{ display: 'flex', gap: '15px', justifyContent: 'center' }}>
          <Share2 size={20} cursor="pointer" />
          <Mail size={20} cursor="pointer" />
        </div>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  const availableDates = Object.keys(newsDatabase).sort().reverse();
  const [currentDate, setCurrentDate] = useState<string>(availableDates[0] || '');
  const [newsletterType, setNewsletterType] = useState<NewsletterType>('general');
  const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null);

  const currentDailyData = newsDatabase[currentDate];
  const currentNews = currentDailyData ? currentDailyData[newsletterType] : [];

  const briefing = newsletterType === 'general' 
    ? "主要企業がモデルの巨大化からニューラル圧縮やエッジベースのマルチモーダル機能へとシフトする中、効率性とアクセシビリティが今日のAIトレンドの中心となっています。"
    : "「チャット」から「アクション」へ。自律的にタスクを遂行し、エージェント同士が連携する『エージェント経済圏』の加速を鮮明に映し出しています。";

  const handleDateChange = (date: string) => {
    setCurrentDate(date);
    setSelectedNews(null);
    window.scrollTo(0, 0);
  };

  const handleTypeChange = (type: NewsletterType) => {
    setNewsletterType(type);
    setSelectedNews(null);
    window.scrollTo(0, 0);
  };

  return (
    <div className="newsletter-container">
      {!selectedNews && (
        <>
          <nav className="date-selector">
            <span className="date-label"><Calendar size={14} /> バックナンバー:</span>
            {availableDates.map(date => (
              <button 
                key={date}
                className={`date-btn ${currentDate === date ? 'active' : ''}`}
                onClick={() => handleDateChange(date)}
              >
                {date.split('-')[2]}日
              </button>
            ))}
          </nav>

          <nav className="newsletter-nav">
            <button 
              className={`nav-item ${newsletterType === 'general' ? 'active' : ''}`}
              onClick={() => handleTypeChange('general')}
            >
              <Newspaper size={18} /> 総合ニュース
            </button>
            <button 
              className={`nav-item ${newsletterType === 'agents' ? 'active' : ''}`}
              onClick={() => handleTypeChange('agents')}
            >
              <Bot size={18} /> エージェント
            </button>
          </nav>
        </>
      )}

      {selectedNews ? (
        <NewsDetail item={selectedNews} date={currentDate} onBack={() => setSelectedNews(null)} />
      ) : (
        <>
          <Header type={newsletterType} date={currentDate} />
          
          <section className="daily-insight">
            <h2>今日のブリーフィング</h2>
            <p>{briefing}</p>
          </section>

          <main>
            {currentNews.length > 0 ? currentNews.map((item, index) => (
              <NewsItemCard 
                key={item.id} 
                item={item} 
                index={index} 
                onReadMore={(news) => {
                  setSelectedNews(news);
                  window.scrollTo(0, 0);
                }} 
              />
            )) : (
              <p style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
                この日のニュースはまだ配信されていません。
              </p>
            )}
          </main>

          <footer>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '20px' }}>
              <Share2 size={20} cursor="pointer" title="シェア" />
              <Mail size={20} cursor="pointer" title="購読" />
              <ExternalLink size={20} cursor="pointer" title="アーカイブ" />
            </div>
            <p>&copy; 2026 {newsletterType === 'general' ? 'AI News Daily' : 'AI Agents Daily'}. 無断複写・転載を禁じます。</p>
            <p style={{ fontSize: '0.7rem', marginTop: '10px' }}>
              このメールは AI News Network の購読者に配信されています。 
              <a href="#" style={{ color: 'inherit', marginLeft: '10px' }}>配信停止はこちら</a>
            </p>
          </footer>
        </>
      )}
    </div>
  );
};

export default App;
