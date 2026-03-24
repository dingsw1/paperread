"""测试模块"""

from filter import assign_category, filter_papers, is_audio_front_end


class TestFilter:
    def test_is_audio_front_end_beamforming(self):
        paper = {"title": "Deep Beamforming for Speech Enhancement", "authors": "Test"}
        assert is_audio_front_end(paper) is True
    
    def test_is_audio_front_end_asr_excluded(self):
        paper = {"title": "End-to-End ASR System", "authors": "Test"}
        assert is_audio_front_end(paper) is False
    
    def test_is_audio_front_end_multimodal_excluded(self):
        paper = {"title": "Audio-Visual Speech Recognition", "authors": "Test"}
        assert is_audio_front_end(paper) is False
    
    def test_assign_category_beamforming(self):
        paper = {"title": "Microphone Array Beamforming"}
        assert assign_category(paper) == "Beamforming"
    
    def test_assign_category_aec(self):
        paper = {"title": "Acoustic Echo Cancellation for VoIP"}
        assert assign_category(paper) == "AEC"
    
    def test_filter_papers(self):
        papers = [
            {"title": "Speech Enhancement", "authors": "A"},
            {"title": "ASR System", "authors": "B"},
        ]
        result = filter_papers(papers)
        assert len(result) == 1
        assert result[0]["title"] == "Speech Enhancement"
