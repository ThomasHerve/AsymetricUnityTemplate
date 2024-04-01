import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UrlService {

  url:string = "https://asyncunitycore.multiplayertournamentonline.fr/"
  constructor(private http: HttpClient) { }

  public publish(id: string |undefined, value: string|undefined) {
    return this.http.post(this.url+id+"/publish", {message: value})
  }
}
