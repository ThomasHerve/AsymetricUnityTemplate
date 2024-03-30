import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-asymetric-unity-template',
  templateUrl: './asymetric-unity-template.component.html',
  styleUrls: ['./asymetric-unity-template.component.css']
})
export class AsymetricUnityTemplateComponent implements OnInit {

  variable: string | undefined;

  constructor(private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.variable = params['variable'];
    });
  }
}
