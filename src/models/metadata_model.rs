use std::rc::Rc;

use finalfusion::prelude::*;
use gtk::prelude::*;
use gtk::ListStore;
use toml::Value;

pub struct MetadataModel {
    inner: ListStore,
}

impl MetadataModel {
    pub fn new(embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>) -> Self {
        let model = ListStore::new(&[String::static_type(), String::static_type()]);

        let model = MetadataModel { inner: model };
        model.update_metadata(&embeddings);

        model
    }

    /// Clear the model.
    fn clear(&self) {
        self.inner.clear();
    }

    pub fn model(&self) -> ListStore {
        self.inner.clone()
    }

    fn update_metadata(&self, embeddings: &Embeddings<VocabWrap, StorageViewWrap>) {
        self.clear();

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
