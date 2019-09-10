import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {
  hwlist: any = [];
  constructor(private http: HttpClient) {
 }

  ngOnInit() {
    this.getData().subscribe(data=>
    {
        this.hwlist = data
    });
  }

  getData(){
    return this.http.get("./student/");
  }

}
