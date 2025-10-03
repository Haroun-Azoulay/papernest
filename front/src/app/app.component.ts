import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { switchMap, map, catchError, distinctUntilChanged } from 'rxjs/operators';
import { timer, of } from 'rxjs';


@Component({
    selector: 'app-notes',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
    imports: [
        CommonModule,
        HttpClientModule,
        RouterLink
    ],
    standalone: true
})
export class AppComponent {
    pingMessage: string = '';

      alive$ = timer(0, 5000).pipe(
    switchMap(() =>
      this.http.get<{ message: string }>('http://localhost:8000/ping').pipe(
        map(({ message }) => (message || '').toLowerCase() === 'pong'),
        catchError(() => of(false))
      )
    ),
    distinctUntilChanged(),

  );

    constructor(private http: HttpClient) { }

}
