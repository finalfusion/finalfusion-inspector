use std::cell::RefCell;
use std::rc::Rc;

use finalfusion::prelude::*;
use gtk::prelude::*;
use gtk::ListStore;
use toml::Value;

use crate::embeddings_ext::EmbeddingsExt;
use crate::models::{EmbeddingsModel, WordStatus};

pub struct MetadataModel {
    embeddings: RefCell<Rc<Embeddings<VocabWrap, StorageViewWrap>>>,
    inner: ListStore,
}

impl MetadataModel {
    pub fn new(embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>) -> Self {
        let model = ListStore::new(&[String::static_type(), String::static_type()]);

        let model = MetadataModel {
            inner: model,
            embeddings: RefCell::new(embeddings),
        };

        model.update_metadata();

        model
    }

    /// Clear the model.
    fn clear(&self) {
        self.inner.clear();
    }

    pub fn model(&self) -> ListStore {
        self.inner.clone()
    }

    fn update_metadata(&self) {
        self.clear();

        let embeddings = self.embeddings.borrow();

        let metadata = match embeddings.metadata() {
            Some(metadata) => metadata,
            None => return,
        };

        let table = match metadata.as_table() {
            Some(table) => table,
            None => return,
        };

        for (key, value) in table {
            let value_string = match value {
                Value::Float(val) => format!("{:.2e}", val),
                other => other.to_string(),
            };
            self.inner
                .insert_with_values(None, &[0, 1], &[key, &value_string]);
        }
    }
}

impl EmbeddingsModel for MetadataModel {
    fn word_status(&self, word: &str) -> WordStatus {
        self.embeddings.borrow().word_status(word)
    }

    fn switch_embeddings(&self, embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>) {
        *self.embeddings.borrow_mut() = embeddings;
        self.update_metadata()
    }
}
