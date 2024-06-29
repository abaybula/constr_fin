import base64
from io import BytesIO

import pandas as pd
from django.db.models import Sum
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from matplotlib import pyplot as plt
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from schedule.forms import PositionForm, ConstructionForm
from schedule.models import Position, Construction
from schedule.permissions import IsUserOnly
from schedule.serializers import ConstructionSerializer, PositionSerializer


class IndexView(APIView):
    """
    View for rendering the index page.
    This view is responsible for rendering the index page when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered response.
    """
    template_name = 'index.html'

    def get(self, request):
        """
        Handle GET requests.
        Renders the index page using the specified template.
        Args:
            request (HttpRequest): The HTTP request object.
        Returns:
            HttpResponse: The rendered response.
        """
        return render(request, self.template_name)


class ConstructionListView(APIView):
    """
    View for rendering the list of constructions.

    This view is responsible for rendering the list of constructions when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered response.
    """
    permission_classes = [IsUserOnly, ]
    queryset = Construction.objects.all()
    serializers_class = ConstructionSerializer
    throttle_classes = [UserRateThrottle, ]
    template_name = 'constructions_list.html'

    def get(self, request, user_id):
        """
        Handle GET requests for the Construction List View.
        This function checks the user's permission, filters the constructions based on the user_id,
        and renders the constructions list template with the filtered constructions.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for filtering constructions.
        Returns:
            HttpResponse: The rendered response with the constructions list.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))
        # Filter constructions based on the user_id
        constructions = Construction.objects.filter(user_id=user_id)
        # Prepare the context data for rendering the template
        context = {
            'constructions': constructions
        }
        # Render the constructions list template with the context data
        return render(request, self.template_name, context)


class AddConstructionView(APIView):
    """
    View for adding a new construction.
    This view is responsible for rendering the construction form when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered response with the construction form.
    """
    permission_classes = [IsUserOnly, ]
    queryset = Construction.objects.all()
    serializers_class = ConstructionSerializer
    throttle_classes = [UserRateThrottle, ]
    template_name = 'add_construction.html'

    def get(self, request, user_id):
        """
        Handle GET requests for the Construction form.
        This function checks if the user has permission to view the page. If not, it returns a 403 Forbidden response.
        If the user has permission, it creates a new instance of the ConstructionForm with the current user as the user_id.
        It then returns a rendered response with the form and the user_id.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form initialization.
        Returns:
            HttpResponse: The rendered response with the form and user_id.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Create a new instance of the ConstructionForm with the current user as the user_id
        form = ConstructionForm(request.user)

        # Create the context with the form and user_id
        context = {
            'form': form,
            'user_id': user_id
        }

        # Return the rendered response with the form and user_id
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        """
        Handle POST requests for adding a new construction.
        This function checks if the user has permission to view the page. If not, it returns a 403 Forbidden response.
        If the user has permission, it creates an instance of the ConstructionForm with the current user and the request data.
        Then, it saves the form and redirects to the constructions list page.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
        Returns:
            HttpResponse: The rendered response with the form and user_id if the form is not valid,
                          or a redirect to the constructions list page if the form is valid.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Create an instance of the ConstructionForm with the current user and the request data
        form = ConstructionForm(request.user, request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Save the form data
            form.save()
            # Redirect to the constructions list page
            return redirect('constructions_list', user_id)

        # Create the context with the form and user_id
        context = {
            'form': form,
            'user_id': user_id
        }

        # Render the response with the form and user_id
        return render(request, self.template_name, context)


class EditConstructionView(APIView):
    """
    View for editing a construction.
    This view is responsible for rendering the construction form when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The user ID for filtering constructions.
    Returns:
        HttpResponse: The rendered response with the construction form.
    """
    permission_classes = [IsUserOnly, ]
    queryset = Construction.objects.all()
    serializers_class = ConstructionSerializer
    throttle_classes = [UserRateThrottle, ]
    template_name = 'edit_construction.html'

    def get(self, request, user_id, construction_id):
        """
        Handle GET requests for editing a construction.
        This function checks if the user has permission to view the page. If not, it returns a 403 Forbidden response.
        If the user has permission, it gets the construction object or returns a 404 if not found.
        It then creates an instance of the ConstructionForm with the current user and the construction object.
        It then returns a rendered response with the form and the user_id.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for filtering constructions.
            construction_id (int): The ID of the construction to edit.
        Returns:
            HttpResponse: The rendered response with the construction form.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Get the construction object or return a 404 if not found
        construction = get_object_or_404(Construction, id=construction_id)

        # Create a form instance for the construction
        form = ConstructionForm(request.user, instance=construction)

        # Create the context with the form and user_id
        context = {
            'form': form,
            'user_id': user_id
        }

        # Render the response with the form and user_id
        return render(request, self.template_name, context)

    def post(self, request, user_id, construction_id):
        """
        Handle POST requests for editing a construction.
        This function checks if the user has permission to view the page. If not, it returns a 403 Forbidden response.
        If the user has permission, it creates an instance of the ConstructionForm with the current user and the request data.
        Then, it saves the form and redirects to the constructions list page.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
            construction_id (int): The ID of the construction to edit.
        Returns:
            HttpResponse: The rendered response with the construction form.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Get the construction object or return a 404 if not found
        construction = get_object_or_404(Construction, id=construction_id)

        # Create a form instance for the construction
        form = ConstructionForm(request.user, request.POST, instance=construction)

        # Check if the form is valid
        if form.is_valid():
            # Save the form data
            form.save()
            # Redirect to the constructions list page
            return redirect('constructions_list', user_id)

        # Create the context with the form and user_id
        context = {
            'form': form,
            'user_id': user_id
        }

        # Render the response with the form and user_id
        return render(request, self.template_name, context)


class DeleteConstructionView(APIView):
    """
    View for deleting a construction.
    This view is responsible for rendering the construction deletion confirmation form when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The user ID for filtering constructions.
    Returns:
        HttpResponse: The rendered response with the construction deletion confirmation form.
    """
    permission_classes = [IsUserOnly, ]
    queryset = Construction.objects.all()
    serializers_class = ConstructionSerializer
    throttle_classes = [UserRateThrottle, ]
    template_name = 'delete_construction.html'

    def get(self, request, user_id, construction_id):
        """
        Handle GET requests for a construction.
        This function checks if the user has permission to view the page. If not, it returns a 403 Forbidden response.
        If the user has permission, it gets the construction object or returns a 404 if not found.
        It then creates a context dictionary with the user_id and construction object.
        Finally, it returns a rendered response with the construction template and context.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for filtering constructions.
            construction_id (int): The ID of the construction to view.
        Returns:
            HttpResponse: The rendered response with the construction template and context.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Get the construction object or return a 404 if not found
        construction = get_object_or_404(Construction, id=construction_id)

        # Create a context dictionary with the user_id and construction object
        context = {
            'user_id': user_id,
            'construction': construction
        }

        # Return a rendered response with the construction template and context
        return render(request, self.template_name, context)

    def post(self, request, user_id, construction_id):
        """
        Handle POST requests for deleting a construction.
        This function checks if the user has permission to view the page. If not, it returns a 403 Forbidden response.
        If the user has permission, it gets the construction object and deletes it.
        Finally, it redirects to the constructions list page.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
            construction_id (int): The ID of the construction to delete.
        Returns:
            HttpResponseRedirect: Redirects to the constructions list page.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Get the construction object or return a 404 if not found
        construction = get_object_or_404(Construction, id=construction_id)

        # Delete the construction
        construction.delete()

        # Redirect to the constructions list page
        return redirect('constructions_list', user_id)


class PositionsListView(APIView):
    """
    View for displaying a list of positions.
    This view is responsible for rendering the positions list page when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The user ID for filtering positions.
        construction_id (int): The ID of the construction to view.
    Returns:
        HttpResponse: The rendered response with the positions list page.
    """
    permission_classes = [IsUserOnly, ]
    queryset = Position.objects.all()
    serializers_class = PositionSerializer
    throttle_classes = [UserRateThrottle, ]
    template_name = 'positions_list.html'

    def get(self, request, user_id, construction_id):
        """
        Get the positions list for a specific construction and render the positions list page.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for filtering positions.
            construction_id (int): The ID of the construction to view.
        Returns:
            HttpResponse: The rendered response with the positions list page.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Get the construction object or return a 404 if not found
        construction = get_object_or_404(Construction, id=construction_id)

        # Get positions related to the construction and order them
        positions = Position.objects.filter(construction=construction).order_by('order')

        # Format the start and end dates of positions
        for position in positions:
            position.start_date = position.start_date.strftime('%d-%m-%Y')
            position.end_date = position.end_date.strftime('%d-%m-%Y')

        # Prepare context data for rendering the template
        context = {
            'user': request.user,
            'construction': construction,
            'positions': positions,
            'total_cost': positions.aggregate(total_cost=Sum('cost'))['total_cost'],
        }

        # Render the positions list page
        return render(request, self.template_name, context)


class AddPositionView(APIView):
    """
    View for adding a position.
    This view is responsible for rendering the add position page when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The user ID for form validation and saving.
        construction_id (int): The ID of the construction to add a position to.
    Returns:
        HttpResponse: The rendered response with the add position page.
    """
    permission_classes = [IsUserOnly, ]
    queryset = Position.objects.all()
    serializers_class = PositionSerializer
    throttle_classes = [UserRateThrottle, ]
    template_name = 'add_position.html'

    def get(self, request, user_id, construction_id):
        """
        Handle GET requests for the AddPositionView.
        This function checks if the user has permission to view the page. If not, it returns a 403 Forbidden response.
        If the user has permission, it creates a new instance of the PositionForm with the current user and the construction ID.
        It then returns a rendered response with the form and the user ID.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
            construction_id (int): The ID of the construction to add a position to.
        Returns:
            HttpResponse: The rendered response with the add position page.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Create a new instance of the PositionForm with the current user and the construction ID
        form = PositionForm(user=request.user, construction_id=construction_id)

        # Prepare context data for rendering the template
        context = {
            'form': form,
            'user': request.user,
            'construction_id': construction_id,
        }

        # Return the rendered response with the form and user ID
        return render(request, self.template_name, context)

    def post(self, request, user_id, construction_id):
        """
        Handle POST requests for adding a new position.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
            construction_id (int): The ID of the construction to add a position to.
        Returns:
            HttpResponse: The rendered response with the added position form if valid,
                          or the form to add a new position.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Create a new instance of the PositionForm with the current user and the construction ID
        form = PositionForm(user=request.user, construction_id=construction_id, data=request.POST)

        # Save the form if it is valid and redirect to the positions list page
        if form.is_valid():
            form.save()
            return redirect('positions_list', user_id=user_id, construction_id=construction_id)

        # Prepare context data for rendering the template with the form and user details
        context = {
            'form': form,
            'user': request.user,
            'construction_id': construction_id,
        }

        # Return the rendered response with the form and user details
        return render(request, self.template_name, context)


class EditPositionView(APIView):
    """
    View for editing a position.
    This view is responsible for rendering the edit position page when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The user ID for form validation and saving.
        construction_id (int): The ID of the construction to add a position to.
        position_id (int): The ID of the position to edit.
    Returns:
        HttpResponse: The rendered response with the edit position page.
    """
    permission_classes = [IsUserOnly, ]
    queryset = Position.objects.all()
    serializers_class = PositionSerializer
    throttle_classes = [UserRateThrottle, ]
    template_name = 'edit_position.html'

    def get(self, request, user_id, construction_id, position_id):
        """
        Handle GET requests for the EditPositionView.
        This function checks if the user has permission to view the page. If not, it returns a 403 Forbidden response.
        If the user has permission, it retrieves the position object or returns a 404 if not found.
        It then creates an instance of the PositionForm with the current user, construction ID, and position object.
        Finally, it renders a response with the form and user details.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
            construction_id (int): The ID of the construction to add a position to.
            position_id (int): The ID of the position to edit.
        Returns:
            HttpResponse: The rendered response with the edit position page.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Retrieve the position object or return a 404 if not found
        position = get_object_or_404(Position, id=position_id)

        # Create a form instance for the position with the current user, construction ID, and position object
        form = PositionForm(request.user, construction_id, instance=position)

        # Prepare context data for rendering the template
        context = {
            'form': form,
            'user': request.user,
            'construction_id': construction_id,
        }

        # Return the rendered response with the form and user details
        return render(request, self.template_name, context)

    def post(self, request, user_id, construction_id, position_id):
        """
        Handle POST requests for editing a position.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
            construction_id (int): The ID of the construction to add a position to.
            position_id (int): The ID of the position to edit.
        Returns:
            HttpResponse: The rendered response with the edit position page.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Retrieve the position object or return a 404 if not found
        position = get_object_or_404(Position, id=position_id)

        # Create a form instance for the position with the current user, construction ID, and position object
        form = PositionForm(user=request.user, construction_id=construction_id, data=request.POST, instance=position)

        # Check if the form is valid and save it if so
        if form.is_valid():
            form.save()
            return redirect('positions_list', user_id=user_id, construction_id=construction_id)

        # Prepare context data for rendering the template with the form and user details
        context = {
            'form': form,
            'user': request.user,
            'construction_id': construction_id,
        }

        # Return the rendered response with the form and user details
        return render(request, self.template_name, context)


class DeletePositionView(APIView):
    """
    View for deleting a position.
    This view is responsible for rendering the delete position page when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The user ID for form validation and saving.
        construction_id (int): The ID of the construction to add a position to.
        position_id (int): The ID of the position to delete.
    Returns:
        HttpResponse: The rendered response with the delete position page.
    """
    permission_classes = [IsUserOnly, ]
    queryset = Position.objects.all()
    serializers_class = PositionSerializer
    throttle_classes = [UserRateThrottle, ]
    template_name = 'delete_position.html'

    def get(self, request, user_id, construction_id, position_id):
        """
        Handle GET requests for deleting a position.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
            construction_id (int): The ID of the construction to add a position to.
            position_id (int): The ID of the position to delete.
        Returns:
            HttpResponse: The rendered response with the delete position page.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            # Return a 403 Forbidden response if the user does not have permission
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Retrieve the position object or return a 404 if not found
        position = get_object_or_404(Position, id=position_id)

        # Prepare context data for rendering the template
        context = {
            'position': position,
            'user': request.user,
            'construction_id': construction_id,
        }

        # Render the template with the context data and return the response
        return render(request, self.template_name, context)

    def post(self, request, user_id, construction_id, position_id):
        """
        Handle POST requests for deleting a position.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
            construction_id (int): The ID of the construction to add a position to.
            position_id (int): The ID of the position to delete.
        Returns:
            HttpResponse: The rendered response with the delete position page.
        """
        # Check if the user has permission to view the page
        if request.user.id != user_id:
            # Return a 403 Forbidden response if the user does not have permission
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Retrieve the position object or return a 404 if not found
        position = get_object_or_404(Position, id=position_id)

        # Delete the position
        position.delete()

        # Redirect to the positions list page
        return redirect('positions_list', user_id, construction_id)


class ScheduleView(APIView):
    """
    View for displaying the schedule.
    This view is responsible for rendering the schedule page when a GET request is made.
    It uses the `render` function from Django to render the template specified by `self.template_name`.
    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The user ID for form validation and saving.
        construction_id (int): The ID of the construction to add a position to.
    Returns:
        HttpResponse: The rendered response with the schedule page.
    """
    permission_classes = [IsUserOnly, ]
    throttle_classes = [UserRateThrottle, ]
    template_name = 'schedule.html'

    def get(self, request, user_id, construction_id):
        """
        View for displaying the schedule.
        This view is responsible for rendering the schedule page when a GET request is made.
        It uses the `render` function from Django to render the template specified by `self.template_name`.
        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The user ID for form validation and saving.
            construction_id (int): The ID of the construction to add a position to.
        Returns:
            HttpResponse: The rendered response with the schedule page.
        """
        if request.user.id != user_id:
            # Return a 403 Forbidden response if the user does not have permission
            return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

        # Get the construction
        construction = get_object_or_404(Construction, id=construction_id)

        # Get all positions for the construction
        positions = Position.objects.filter(construction=construction).order_by('order')

        # Calculate cost per day for each position and create dataframe for plotting the cost schedule
        if positions:
            data = {'Position': [], 'Cost': [], 'Month': []}
            for position in positions:
                start_date = position.start_date
                end_date = position.end_date

                if start_date > end_date:
                    start_date, end_date = end_date, start_date

                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)

                if position.name == 'other':
                    position.name = position.other_name

                if position.cost == 0 or end_date == start_date:
                    return

                position.days = (end_date - start_date).days

                cost_per_day = position.cost / (end_date - start_date).days

                # Create dataframe for plotting the cost schedule
                for i in range((end_date - start_date).days):
                    data['Position'].append(position.name)
                    data['Cost'].append(cost_per_day)
                    data['Month'].append(start_date.strftime('%m-%Y'))
                    start_date += pd.Timedelta(days=1)

            # Convert to pandas dataframe for plotting the cost schedule
            df = pd.DataFrame(data)

            # Calculate monthly cost, position monthly cost, position and total cost for plotting the cost schedule
            df['Month'] = pd.to_datetime(df['Month'], format='%m-%Y')
            monthly_cost = df.groupby('Month')['Cost'].sum().reset_index()
            position_monthly_cost = df.groupby(['Month', 'Position'])['Cost'].sum().reset_index()
            position_cost = df.groupby('Position')['Cost'].sum().reset_index()
            total_cost = df['Cost'].sum()

            # Get position parameters for plotting the cost schedule
            position_names = {position.name: _(position.name) for position in positions}
            names = [position.name for position in positions]
            start_dates = [position.start_date for position in positions]
            end_dates = [position.end_date for position in positions]

            # Plot monthly cost schedule
            fig, ax_main = plt.subplots(figsize=(18, 12), constrained_layout=True, dpi=300)
            for i in range(len(names)):
                ax_main.barh([names[i]], [end_dates[i] - start_dates[i]], left=[start_dates[i]], color='b', alpha=0.3,
                             align='edge', height=0.4, edgecolor='black', linewidth=2, zorder=1, label=names[i])

            # Plot monthly cost
            for i, row in monthly_cost.iterrows():
                try:
                    month_date = pd.to_datetime(row['Month'], format='%m-%Y')
                    ax_main.text(month_date, len(names) - 0.1, f"{row['Cost']:,.0f}", ha='left', fontsize=12)
                except Exception as e:
                    return HttpResponse(f"Error plotting cost information: {e}")

            # Plot position monthly cost
            for i, row in position_monthly_cost.iterrows():
                try:
                    position_index = names.index(row['Position'])
                    position_month_date = pd.to_datetime(row['Month'], format='%m-%Y')
                    ax_main.text(position_month_date, position_index - 0.1, f"{row['Cost']:,.0f}", ha='left',
                                 fontsize=12)
                except Exception as e:
                    return HttpResponse(f"Error plotting cost information: {e}")

            # Plot position cost
            for i, row in position_cost.iterrows():
                try:
                    position_index = names.index(row['Position'])
                    ax_main.text(max(end_dates), position_index - 0.1, f"{row['Cost']:,.0f}", ha='left', fontsize=12)
                except Exception as e:
                    return HttpResponse(f"Error plotting cost information: {e}")

            # Plot total
            plt.figtext(0.93, 0.03, f"Total: {total_cost:,.0f}", horizontalalignment='left', fontsize=12)

            # Set ticks and tick labels for x and y axes
            ax_main.tick_params(labelsize=12, width=0)
            ax_main.set_yticklabels(list(position_names.values()))
            ax_main.set_xticklabels(pd.date_range(min(start_dates), max(end_dates), freq='MS').strftime('%b-%Y'),
                                    ha='left')

            # Set x and y limits and grid
            ax_main.set_xlim(min(start_dates), max(end_dates))
            ax_main.set_ylim(-0.5, len(names))
            ax_main.grid(axis='x', zorder=0, alpha=0.3, linewidth=0.3, color='grey')
            ax_main.grid(axis='y', zorder=0, alpha=0.3, linewidth=0.3, color='grey')
            ax_main.invert_yaxis()

            # Sets the title if a construct name is specified in the URL
            if construction is None:
                ax_main.set_title('')
            else:
                ax_main.set_title(construction, fontsize=20)

            # Delete spines on the top, right, bottom, and left
            ax_main.spines['top'].set_visible(False)
            ax_main.spines['right'].set_visible(False)
            ax_main.spines['bottom'].set_visible(False)
            ax_main.spines['left'].set_visible(False)

            # Adjust layout and save image
            fig.tight_layout()
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300, transparent=True)
            plt.close()
            buffer.seek(0)

            # Convert plot to base64 image
            schedule_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()

            # Generate PDF from plot image
            if 'download_pdf' in request.GET:
                pdf_buffer = BytesIO()
                fig.savefig(pdf_buffer, format='pdf', bbox_inches='tight', pad_inches=0.1, transparent=True)
                pdf_buffer.seek(0)

                # Set content disposition and return response
                response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="schedule.pdf"'
                pdf_buffer.close()
                return response
            # Render template
            return render(request, 'schedule.html', {'schedule_image': schedule_image, 'construction': construction})
        else:
            # Render template with no schedule
            return render(request, 'schedule.html', {})
