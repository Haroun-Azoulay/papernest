import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { AppSearch } from './app.search';


export const routes: Routes = [

  {    path: '',
       component: AppComponent,
  },

   {   path: 'search',
       component: AppSearch,
  },

];
