<template>
  <div>
    <nav-bar></nav-bar>
    <Container>
      <div>
        <b-card title="Authors">
          <div class="mb-3">
            <b-form-input v-model="searchText" placeholder="Search authors" @input="filterAuthors"></b-form-input>
            <b-button @click="showAddModal" variant="success" class="mt-3">Add New Author</b-button>
          </div>
          <b-table striped hover :items="filteredAuthors" :fields="tableFields">
            <template #cell(actions)="row">
              <b-button @click="editAuthor(row.item)" variant="primary" size="sm">Edit</b-button>
            </template>
          </b-table>
        </b-card>

        <!-- Add Author Modal -->
        <b-modal hide-footer v-model="addModal" title="Add Author">
          <b-form @submit.prevent="addAuthor">
            <b-form-group label="Name">
              <b-form-input v-model="newAuthor.name" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Save</b-button>
            <b-button @click="hideAddModal" variant="secondary">Cancel</b-button>
          </b-form>
        </b-modal>

        <!-- Add Book Modal -->
        <b-modal hide-footer v-model="addBookModal" title="Add Book">
          <b-form @submit.prevent="addBook">
            <b-form-group label="Book Title">
              <b-form-input v-model="newBook.title" required></b-form-input>
            </b-form-group>
            <b-form-group label="Number of pages">
              <b-form-input v-model="newBook.pages" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Save</b-button>
            <b-button @click="hideAddBookModal" variant="secondary">Cancel</b-button>
          </b-form>
        </b-modal>

        <!-- Edit Author Modal -->
        <b-modal hide-footer v-if="editModal" v-model="editModal" title="Edit Author">
          <b-form @submit.prevent="updateAuthor">
          <b-form-group label="Name">
            <b-form-input v-model="selectedAuthor.name" required></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Save</b-button>
          <b-button @click="hideEditModal" variant="secondary">Cancel</b-button>
        </b-form>
          <b-card title="Books" class="mt-3">
            <b-table striped hover :items="selectedAuthor.books" :fields="bookTableFields">
              <template #cell(actions)="row">
                <b-button @click="editBook(row.item)" variant="primary" size="sm">Edit</b-button>
                <b-button @click="deleteBook(row.item)" variant="danger" size="sm">Delete</b-button>
              </template>
            </b-table>
            <b-button @click="showAddBookModal" variant="success" class="mt-3">Add New Book</b-button>
          </b-card>
        </b-modal>

        <!-- Edit Book Modal -->
        <b-modal hide-footer v-if="editBookModal" v-model="editBookModal" title="Edit Book">
          <b-form @submit.prevent="updateBook">
            <b-form-group label="Book Title">
              <b-form-input v-model="selectedBook.title" required></b-form-input>
            </b-form-group>
            <b-form-group label="Number of Pages">
              <b-form-input v-model="selectedBook.pages" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Save</b-button>
            <b-button @click="hideEditBookModal" variant="secondary">Cancel</b-button>
          </b-form>
        </b-modal>
      </div>
    </Container>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator';
import {getAccessToken} from "~/helpers/localStorageUtils";

@Component({})
export default class Authors extends Vue {
  private searchText: string = '';
  private authors: any[] = [];
  private filteredAuthors: any[] = [];
  private addModal: boolean = false;
  private editModal: boolean = false;
  private selectedAuthor: any = null;
  private accessToken: string = ''
  private newAuthor: any = {
    name: ''
  }

  private tableFields: any[] = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'num_books', label: 'Number of Books' },
    { key: 'actions', label: 'Actions' },
  ];

  private addBookModal: boolean = false;
  private editBookModal: boolean = false;
  private selectedBook: any = null;
  private newBook: any = {
    title: '',
    pages: 0,
  };

  private bookTableFields: any[] = [
    { key: 'title', label: 'Book Title' },
    { key: 'pages', label: 'Number of Pages' },
    { key: 'actions', label: 'Actions' },
  ];


  async mounted(): Promise<void> {
    await this.fetchAuthors();
  }

  async fetchAuthors(): Promise<void> {
    try {
      const accessToken: string | null = getAccessToken();
      if (!accessToken) {
        await this.$router.push('/login');
      }
      this.accessToken = accessToken!
      const response = await this.$axios.get('/author/all/', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      this.authors = response.data.authors
      this.filteredAuthors = response.data.authors
    } catch (error: any) {
      if (error.response && error.response.status === 401) {
        await this.$router.push('/login');
      }else{
        console.error(error);
      }
    }
  }

  filterAuthors() {
    this.filteredAuthors = this.authors.filter(author =>
      author.name.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }

  showAddModal() {
    this.addModal = true;
  }

  hideAddModal() {
    this.addModal = false;
  }

  editAuthor(author: any) {
    this.selectedAuthor = {...author};
    this.editModal = true;
  }

  hideEditModal() {
    this.selectedAuthor = null;
    this.editModal = false;
  }

  async addAuthor() {
    await this.$axios.post('/author', this.newAuthor, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      });
    await this.fetchAuthors();
    this.newAuthor = {
      name: ''
    }
    this.hideAddModal();
  }

  async updateAuthor() {
    await this.$axios.put(`/author/${this.selectedAuthor.id}`, { name: this.selectedAuthor.name}, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      });
    await this.fetchAuthors();
    this.hideEditModal();
  }

  showAddBookModal() {
    this.addBookModal = true;
  }

  hideAddBookModal() {
    this.addBookModal = false;
  }

  editBook(book: any) {
    this.selectedBook = { ...book };
    this.editBookModal = true;
  }

  hideEditBookModal() {
    this.selectedBook = null;
    this.editBookModal = false;
  }

  async addBook() {
    await this.$axios.post(`/book`, {...this.newBook, author_id: this.selectedAuthor.id}, {
      headers: {
        Authorization: `Bearer ${this.accessToken}`,
      }
    });
    await this.fetchAuthors();
    this.newBook = {
      title: '',
      pages: 0,
    }
    this.hideAddBookModal();
    this.hideEditModal();
  }

  async updateBook() {
    await this.$axios.put(`/book/${this.selectedBook.id}`, this.selectedBook, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      });
    await this.fetchAuthors();
    this.hideEditBookModal();
    this.hideEditModal();
  }

  async deleteBook(book: any) {
    if (confirm("Are you sure you want to delete this book?")){
      await this.$axios.delete(`/book/${book.id}`, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        }
      });
      await this.fetchAuthors();
      this.hideEditBookModal();
      this.hideEditModal();
    }
  }
}
</script>
