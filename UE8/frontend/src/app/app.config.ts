import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import {provideHttpClient} from "@angular/common/http";
import { provideAnimations } from '@angular/platform-browser/animations';
import {StarRatingConfig, StarRatingConfigService, StarRatingModule} from "angular-star-rating";

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    provideAnimations(),
    StarRatingConfigService
],
};
