import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AsymetricUnityTemplateComponent } from './asymetric-unity-template.component';

describe('AsymetricUnityTemplateComponent', () => {
  let component: AsymetricUnityTemplateComponent;
  let fixture: ComponentFixture<AsymetricUnityTemplateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AsymetricUnityTemplateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AsymetricUnityTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
