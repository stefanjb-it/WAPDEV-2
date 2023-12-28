import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {KeyValueItem} from "./models/KeyValueItem";

@Injectable({
  providedIn: 'root'
})
export class CountryService {

  constructor(private http:HttpClient) { }

  getCountries() {
    return this.http.get<KeyValueItem[]>('/api/countries');
  }
}
