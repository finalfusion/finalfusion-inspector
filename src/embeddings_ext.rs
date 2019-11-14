use finalfusion::prelude::*;
use finalfusion::similarity::{Analogy, WordSimilarityResult};
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
    /// Performs analogy queries with any type `AsRef<str>`.
    ///
    /// Can be removed when finalfusion relaxes the signature.
    fn analogy_flexible(
        &self,
        words: [impl AsRef<str>; 3],
        limit: usize,
    ) -> Result<Vec<WordSimilarityResult>, [bool; 3]>;

    fn word_status(&self, word: &str) -> WordStatus;
}

impl EmbeddingsExt for Embeddings<VocabWrap, StorageViewWrap> {
    fn analogy_flexible(
        &self,
        words: [impl AsRef<str>; 3],
        limit: usize,
    ) -> Result<Vec<WordSimilarityResult>, [bool; 3]> {
        self.analogy(
            [words[0].as_ref(), words[1].as_ref(), words[2].as_ref()],
            limit,
        )
    }

    fn word_status(&self, word: &str) -> WordStatus {
        match self.vocab().idx(word) {
            Some(WordIndex::Word(_)) => WordStatus::Known,
            Some(WordIndex::Subword(_)) => WordStatus::Subword,
            None => WordStatus::Unknown,
        }
    }
}
