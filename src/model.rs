use finalfusion::prelude::*;
use finalfusion::vocab::{Vocab, WordIndex};

#[derive(Clone, Copy, Eq, PartialEq)]
pub enum WordStatus {
    Known,
    Subword,
    Unknown,
}

impl WordStatus {
    pub fn is_valid(self) -> bool {
        use WordStatus::*;

        match self {
            Known => true,
            Subword => true,
            Unknown => false,
        }
    }
}

pub trait EmbeddingsExt {
    fn word_status(&self, word: &str) -> WordStatus;
}

impl EmbeddingsExt for Embeddings<VocabWrap, StorageViewWrap> {
    fn word_status(&self, word: &str) -> WordStatus {
        match self.vocab().idx(word) {
            Some(WordIndex::Word(_)) => WordStatus::Known,
            Some(WordIndex::Subword(_)) => WordStatus::Subword,
            None => WordStatus::Unknown,
        }
    }
}

pub trait EmbeddingsModel {
    fn embeddings(&self) -> &Embeddings<VocabWrap, StorageViewWrap>;
}
