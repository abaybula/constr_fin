import base64
from io import BytesIO

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from matplotlib import pyplot as plt
from rest_framework.decorators import api_view, permission_classes

from schedule.forms import PositionForm, ConstructionForm
from schedule.models import Position, Construction
from schedule.permissions import IsUserOnly


def index(request):
    """
    Renders the 'index.html' template and returns the rendered HTML as an HttpResponse object.
    Parameters:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered HTML response.
    """
    return render(request, 'index.html')


@login_required
@api_view(['GET'])
@permission_classes([IsUserOnly])
def positions_list(request, user_id):
    """
    Retrieves a list of positions for a specific user and renders the 'positions_list.html' template.
    Parameters:
        request (HttpRequest): The HTTP request object.
        user_id (int): The ID of the user.
    Returns:
        HttpResponse: The rendered HTML response containing the positions list, construction name, and total cost.
    Raises:
        HttpResponseForbidden: If the user is not authorized to view the page.
    """
    if request.user.id != user_id:
        return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

    construction = Construction.objects.filter(user_id=user_id).first()

    positions = Position.objects.filter(user_id=user_id).order_by('order')

    for position in positions:
        position.start_date = position.start_date.strftime('%d-%m-%Y')
        position.end_date = position.end_date.strftime('%d-%m-%Y')

    total_cost = sum(position.cost for position in positions)

    return render(request, 'positions_list.html',
                  {'construction': construction, 'positions': positions, 'total_cost': total_cost})


@login_required
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsUserOnly])
def add_construction_name(request, user_id):
    """
    Add a new construction name for a user.
    This view function handles both GET and POST requests. It requires the user to be logged in and have the necessary
    permissions.
    Parameters:
        - request (HttpRequest): The HTTP request object.
        - user_id (int): The ID of the user.
    Returns:
        - HttpResponseRedirect: If the construction name is successfully added and saved, redirects to the
        'positions_list' view with the user ID.
        - HttpResponseForbidden: If the user is not authorized to view the page.
        - HttpResponse: If the request method is GET, renders the 'add_construction_name.html' template with the form.
    """
    if request.user.id != user_id:
        return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

    if request.method == 'POST':
        form = ConstructionForm(request.POST)
        if form.is_valid():
            construction = form.save(commit=False)
            construction.user_id = user_id
            construction.save()
            return redirect('positions_list', user_id=user_id)
    else:
        form = ConstructionForm()
    return render(request, 'add_construction_name.html', {'form': form})


@login_required
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsUserOnly])
def edit_construction_name(request, user_id, pk):
    """
    Edit the construction name.
    This view function is responsible for editing the construction name. It requires the user to be logged in and have
    the permission to view the page. The user ID and the primary key (pk) of the construction name to be edited are
    obtained from the request parameters.
    Parameters:
        - request: The HTTP request object.
        - user_id: The ID of the user.
        - pk: The primary key of the construction name.
    Returns:
        - HttpResponseForbidden: If the user is not authorized to view the page.
        - HttpResponse: If the request method is GET, renders the 'edit_construction_name.html' template with the form
        and the construction object.
    Raises:
        - None
    """
    if request.user.id != user_id:
        return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

    construction = get_object_or_404(Construction, pk=pk, user_id=user_id)

    if request.method == 'POST':
        form = ConstructionForm(request.POST, instance=construction)
        if form.is_valid():
            form.save()
            return redirect('positions_list', user_id=user_id)
    else:
        form = ConstructionForm(instance=construction)

    return render(request, 'edit_construction_name.html', {'form': form, 'construction': construction})


@login_required
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsUserOnly])
def delete_construction_name(request, user_id, pk):
    """
    Delete the construction name.
    This view function is responsible for deleting the construction name. It requires the user to be logged in and have
    the permission to view the page. The user ID and the primary key (pk) of the construction name to be deleted are
    obtained from the request parameters.
    Parameters:
        - request: The HTTP request object.
        - user_id: The ID of the user.
        - pk: The primary key of the construction name.
    Returns:
        - HttpResponseForbidden: If the user is not authorized to view the page.
        - HttpResponse: If the request method is GET, renders the 'delete_construction_name.html' template with the
        construction object.
    Raises:
        - None
    """
    if request.user.id != user_id:
        return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

    construction = get_object_or_404(Construction, pk=pk, user_id=user_id)

    if request.method == 'POST':
        construction.delete()
        return redirect('positions_list', user_id=user_id)

    return render(request, 'delete_construction_name.html', {'construction': construction})


@login_required
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsUserOnly])
def add_position(request, user_id):
    """
    Add a new position for a user.
    This view function handles both GET and POST requests. It requires the user to be logged in and have the necessary
     permissions.
    Parameters:
        - request (HttpRequest): The HTTP request object.
        - user_id (int): The ID of the user.
    Returns:
        - HttpResponseForbidden: If the user is not authorized to view the page.
        - HttpResponse: If the request method is GET, renders the 'add_position.html' template with the form.
        - HttpResponseRedirect: If the position is successfully added and saved, redirects to the 'positions_list' view
         with the user ID.
    Raises:
        - None
    """
    if request.user.id != user_id:
        return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

    position = Position(user_id=user_id)
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['name'] == 'other':
                position.name = form.cleaned_data['other_name']
            else:
                position.name = form.cleaned_data['name']
            position = form.save(commit=False)
            position.user_id = user_id
            try:
                position.save()
                return redirect('positions_list', user_id=user_id)
            except Exception as e:
                form.add_error(None, _("Error saving position: {error}".format(error=str(e))))
    else:
        form = PositionForm()

    return render(request, 'add_position.html', {'form': form})


@login_required
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsUserOnly])
def edit_position(request, user_id, pk):
    """
    Edit an existing position for a user.
    This view function handles both GET and POST requests. It requires the user to be logged in and have the necessary
     permissions.
    Parameters:
        - request (HttpRequest): The HTTP request object.
        - user_id (int): The ID of the user.
        - pk (int): The primary key of the position to be edited.
    Returns:
        - HttpResponseForbidden: If the user is not authorized to view the page.
        - HttpResponse: If the request method is GET, renders the 'edit_position.html' template with the form and the
         position object.
        - HttpResponseRedirect: If the position is successfully edited and saved, redirects to the 'positions_list' view
         with the user ID.
    Raises:
        - None
    """
    if request.user.id != user_id:
        return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

    position = get_object_or_404(Position, pk=pk)

    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            if form.cleaned_data['name'] == 'other':
                position.name = form.cleaned_data['other_name']
            else:
                position.name = form.cleaned_data['name']
            position = form.save(commit=False)
            position.user_id = user_id
            try:
                position.save()
                return redirect('positions_list', user_id=user_id)
            except Exception as e:
                form.add_error(None, _("Error saving position: {error}".format(error=str(e))))
    else:
        form = PositionForm(instance=position)

    return render(request, 'edit_position.html', {'form': form})


@login_required
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsUserOnly])
def delete_position(request, user_id, pk):
    """
    Delete an existing position for a user.
    This view function handles both GET and POST requests. It requires the user to be logged in and have the necessary
     permissions.
    Parameters:
        - request (HttpRequest): The HTTP request object.
        - user_id (int): The ID of the user.
        - pk (int): The primary key of the position to be deleted.
    Returns:
        - HttpResponseForbidden: If the user is not authorized to view the page.
        - HttpResponse: If the request method is GET, renders the 'delete_position.html' template with the position
         object.
        - HttpResponseRedirect: If the position is successfully deleted, redirects to the 'positions_list' view with the
         user ID.
    Raises:
        - None
    """
    if request.user.id != user_id:
        return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

    position = get_object_or_404(Position, pk=pk)

    if request.method == 'POST':
        position.delete()
        return redirect('positions_list', user_id=user_id)

    return render(request, 'delete_position.html', {'position': position})


@login_required
@api_view(['GET'])
@permission_classes([IsUserOnly])
def schedule(request, user_id):
    """
    View the schedule for a user.
    This view function handles GET requests. It requires the user to be logged in and have the necessary permissions.
    Parameters:
        - request (HttpRequest): The HTTP request object.
        - user_id (int): The ID of the user.
    Returns:
        - HttpResponseForbidden: If the user is not authorized to view the page.
        - HttpResponse: If the request method is GET, renders the 'schedule.html' template with the positions and
         construction object.
    Raises:
        - None
    """
    if request.user.id != user_id:
        return HttpResponseForbidden(_("<h1>You don't have permission to view this page</h1>"))

    construction = Construction.objects.filter(user_id=user_id).first()

    positions = Position.objects.filter(user_id=user_id).order_by('order')

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

        # Plot total cost
        plt.figtext(0.93, 0.03, f"Total: {total_cost:,.0f}", horizontalalignment='left', fontsize=12)

        # Set ticks and tick labels for x and y axes
        ax_main.tick_params(labelsize=12, width=0)
        ax_main.set_yticklabels(list(position_names.values()))
        ax_main.set_xticklabels(pd.date_range(min(start_dates), max(end_dates), freq='MS').strftime('%b %Y'), ha='left')

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
            ax_main.set_title(construction.construction_name, fontsize=20)

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
        return render(request, 'schedule.html', {'schedule_image': schedule_image})
    else:
        # Render template with no schedule
        return render(request, 'schedule.html', {})